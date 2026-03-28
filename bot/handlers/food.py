import logging
import io

from aiogram import Router, F, Bot
from bot.config import settings
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards.food import food_result_keyboard, food_saved_keyboard
from bot.locales import t
from bot.models.user import User
from bot.services.diary_service import DiaryService
from bot.services.openai_service import OpenAIService
from openai import OpenAIError

logger = logging.getLogger(__name__)
router = Router()
openai_service = OpenAIService()


class FoodStates(StatesGroup):
    waiting_grams = State()


def _build_result_text(lang: str, dish_name: str, grams: int, calories: float,
                       protein: float, fat: float, carbs: float, description: str) -> str:
    return t(
        "food_result",
        lang,
        dish_name=dish_name,
        grams=grams,
        calories=round(calories),
        protein=round(protein, 1),
        fat=round(fat, 1),
        carbs=round(carbs, 1),
        description=description,
    )


@router.message(F.photo)
async def handle_food_photo(
    message: Message,
    bot: Bot,
    db_user: User,
    lang: str,
    session: AsyncSession,
    state: FSMContext,
):
    if not db_user.is_onboarded:
        from bot.keyboards.onboarding import language_keyboard
        await message.answer(
            t("welcome", lang),
            reply_markup=language_keyboard(),
            parse_mode="HTML",
        )
        return

    await bot.send_chat_action(message.chat.id, "typing")
    loading_msg = await message.answer(t("food_analyzing", lang), parse_mode="HTML")

    # Log all incoming photos to channel immediately
    photo = message.photo[-1]
    username = f"@{message.from_user.username}" if message.from_user.username else "—"
    name = db_user.name or message.from_user.first_name or "—"
    log_caption = (
        f"📸 <b>Фото от пользователя</b>\n"
        f"ID: <code>{db_user.telegram_id}</code>\n"
        f"Username: {username}\n"
        f"Имя: {name}"
    )
    try:
        await bot.send_photo(
            settings.LOG_CHANNEL_ID,
            photo=photo.file_id,
            caption=log_caption,
            parse_mode="HTML",
        )
    except Exception as e:
        logger.warning(f"Failed to send photo to log channel: {e}")

    try:
        file = await bot.get_file(photo.file_id)

        buf = io.BytesIO()
        await bot.download_file(file.file_path, buf)
        photo_bytes = buf.getvalue()

        result = await openai_service.analyze_food_photo(photo_bytes, lang=lang)

        if not result or not result.is_food:
            await loading_msg.edit_text(
                t("food_not_detected", lang),
                parse_mode="HTML",
            )
            return

        # Store analysis in FSM state (not saved yet)
        response_text = _build_result_text(
            lang, result.dish_name, result.grams,
            result.calories, result.protein, result.fat, result.carbs,
            result.description,
        )

        await loading_msg.edit_text(
            response_text,
            reply_markup=food_result_keyboard(lang),
            parse_mode="HTML",
        )

        await state.set_data({
            "dish_name": result.dish_name,
            "grams": result.grams,
            "calories": result.calories,
            "protein": result.protein,
            "fat": result.fat,
            "carbs": result.carbs,
            "description": result.description,
            "photo_file_id": photo.file_id,
            "result_message_id": loading_msg.message_id,
            # per-gram ratios for recalculation
            "cal_per_gram": result.calories / result.grams if result.grams else 0,
            "prot_per_gram": result.protein / result.grams if result.grams else 0,
            "fat_per_gram": result.fat / result.grams if result.grams else 0,
            "carbs_per_gram": result.carbs / result.grams if result.grams else 0,
        })

    except OpenAIError as e:
        logger.error(f"OpenAI error for user {db_user.telegram_id}: {e}")
        await loading_msg.edit_text(t("food_api_error", lang), parse_mode="HTML")
    except Exception as e:
        logger.error(f"Unexpected error analyzing food for user {db_user.telegram_id}: {e}")
        await loading_msg.edit_text(t("error_general", lang), parse_mode="HTML")


@router.callback_query(F.data == "food:save")
async def cb_food_save(
    callback: CallbackQuery,
    db_user: User,
    lang: str,
    session: AsyncSession,
    state: FSMContext,
):
    data = await state.get_data()
    if not data or "dish_name" not in data:
        await callback.answer()
        return

    diary_service = DiaryService(session)
    await diary_service.add_entry(
        user_id=db_user.telegram_id,
        dish_name=data["dish_name"],
        calories=data["calories"],
        protein=data["protein"],
        fat=data["fat"],
        carbs=data["carbs"],
        description=data.get("description", ""),
        photo_file_id=data.get("photo_file_id"),
    )
    await state.clear()

    await callback.message.edit_text(
        t("food_saved_success", lang),
        reply_markup=food_saved_keyboard(lang),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "food:edit_grams")
async def cb_food_edit_grams(
    callback: CallbackQuery,
    lang: str,
    state: FSMContext,
):
    data = await state.get_data()
    if not data or "dish_name" not in data:
        await callback.answer()
        return

    ask_msg = await callback.message.answer(t("food_ask_grams", lang), parse_mode="HTML")
    await state.update_data(ask_grams_message_id=ask_msg.message_id)
    await state.set_state(FoodStates.waiting_grams)
    await callback.answer()


@router.message(FoodStates.waiting_grams)
async def handle_grams_input(
    message: Message,
    bot: Bot,
    db_user: User,
    lang: str,
    state: FSMContext,
):
    data = await state.get_data()
    if not data or "dish_name" not in data:
        await state.clear()
        return

    # Delete user's input message and the "ask grams" prompt
    try:
        await message.delete()
    except Exception:
        pass
    ask_msg_id = data.get("ask_grams_message_id")
    if ask_msg_id:
        try:
            await bot.delete_message(message.chat.id, ask_msg_id)
        except Exception:
            pass

    try:
        new_grams = int(message.text.strip())
        if new_grams <= 0:
            raise ValueError
    except (ValueError, AttributeError):
        err_msg = await bot.send_message(
            message.chat.id, t("food_grams_invalid", lang), parse_mode="HTML"
        )
        await state.update_data(ask_grams_message_id=err_msg.message_id)
        return

    # Recalculate based on per-gram ratios
    new_calories = data["cal_per_gram"] * new_grams
    new_protein = data["prot_per_gram"] * new_grams
    new_fat = data["fat_per_gram"] * new_grams
    new_carbs = data["carbs_per_gram"] * new_grams

    await state.update_data(
        grams=new_grams,
        calories=new_calories,
        protein=new_protein,
        fat=new_fat,
        carbs=new_carbs,
        ask_grams_message_id=None,
    )
    await state.set_state(None)

    response_text = _build_result_text(
        lang, data["dish_name"], new_grams,
        new_calories, new_protein, new_fat, new_carbs,
        data["description"],
    )

    # Edit the original result message
    result_msg_id = data.get("result_message_id")
    if result_msg_id:
        try:
            await bot.edit_message_text(
                text=response_text,
                chat_id=message.chat.id,
                message_id=result_msg_id,
                reply_markup=food_result_keyboard(lang),
                parse_mode="HTML",
            )
            return
        except Exception:
            pass

    # Fallback: send new message
    await bot.send_message(
        message.chat.id,
        response_text,
        reply_markup=food_result_keyboard(lang),
        parse_mode="HTML",
    )
