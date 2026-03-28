import logging

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards.profile import profile_keyboard, gender_edit_keyboard, goal_edit_keyboard
from bot.keyboards.main_menu import main_menu_keyboard
from bot.locales import t
from bot.models.user import User
from bot.services.user_service import UserService

logger = logging.getLogger(__name__)
router = Router()


class ProfileEditStates(StatesGroup):
    editing_name = State()
    editing_age = State()
    editing_height = State()
    editing_weight = State()


def _build_profile_text(user: User, lang: str) -> str:
    gender_map = {"male": t("gender_male", lang), "female": t("gender_female", lang)}
    goal_map = {
        "lose": t("goal_lose", lang),
        "maintain": t("goal_maintain", lang),
        "gain": t("goal_gain", lang),
    }
    return t(
        "profile_title",
        lang,
        name=user.name or "—",
        age=user.age or "—",
        gender=gender_map.get(user.gender, "—"),
        height=user.get_height_display(),
        weight=user.get_weight_display(),
        goal=goal_map.get(user.goal, "—"),
        calories=int(user.daily_calories) if user.daily_calories else "—",
    )


@router.callback_query(F.data == "menu:profile")
async def cb_profile(callback: CallbackQuery, db_user: User, lang: str):
    text = _build_profile_text(db_user, lang)
    await callback.message.edit_text(
        text,
        reply_markup=profile_keyboard(lang),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "profile:edit:name")
async def cb_edit_name(callback: CallbackQuery, state: FSMContext, lang: str):
    await state.set_state(ProfileEditStates.editing_name)
    await callback.message.edit_text(
        t("onboarding_name_ask", lang),
        parse_mode="HTML",
    )
    await callback.answer()


@router.message(ProfileEditStates.editing_name)
async def process_edit_name(message: Message, state: FSMContext, db_user: User, lang: str, session: AsyncSession):
    name = message.text.strip()
    if not name or len(name) > 64:
        await message.answer(t("error_invalid_input", lang))
        return

    user_service = UserService(session)
    updated = await user_service.update_user(db_user.telegram_id, name=name)
    await state.clear()
    await message.answer(
        t("profile_updated", lang) + "\n\n" + _build_profile_text(updated, lang),
        reply_markup=profile_keyboard(lang),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "profile:edit:age")
async def cb_edit_age(callback: CallbackQuery, state: FSMContext, lang: str):
    await state.set_state(ProfileEditStates.editing_age)
    await callback.message.edit_text(
        t("onboarding_age_ask", lang),
        parse_mode="HTML",
    )
    await callback.answer()


@router.message(ProfileEditStates.editing_age)
async def process_edit_age(message: Message, state: FSMContext, db_user: User, lang: str, session: AsyncSession):
    try:
        age = int(message.text.strip())
        if not (10 <= age <= 100):
            raise ValueError
    except ValueError:
        await message.answer(t("onboarding_age_invalid", lang))
        return

    user_service = UserService(session)
    updated = await user_service.update_user(db_user.telegram_id, age=age)
    await state.clear()
    await message.answer(
        t("profile_updated", lang) + "\n\n" + _build_profile_text(updated, lang),
        reply_markup=profile_keyboard(lang),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "profile:edit:gender")
async def cb_edit_gender(callback: CallbackQuery, lang: str):
    await callback.message.edit_text(
        t("onboarding_gender_ask", lang),
        reply_markup=gender_edit_keyboard(lang),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("profile:set:gender:"))
async def cb_set_gender(callback: CallbackQuery, db_user: User, lang: str, session: AsyncSession):
    gender = callback.data.split(":")[-1]
    user_service = UserService(session)
    updated = await user_service.update_user(db_user.telegram_id, gender=gender)
    await callback.message.edit_text(
        t("profile_updated", lang) + "\n\n" + _build_profile_text(updated, lang),
        reply_markup=profile_keyboard(lang),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "profile:edit:height")
async def cb_edit_height(callback: CallbackQuery, state: FSMContext, db_user: User, lang: str):
    await state.set_state(ProfileEditStates.editing_height)
    key = "onboarding_height_ask" if db_user.units == "metric" else "onboarding_height_ask_imperial"
    await callback.message.edit_text(t(key, lang), parse_mode="HTML")
    await callback.answer()


@router.message(ProfileEditStates.editing_height)
async def process_edit_height(message: Message, state: FSMContext, db_user: User, lang: str, session: AsyncSession):
    try:
        raw = float(message.text.strip().replace(",", "."))
        if db_user.units == "imperial":
            feet = int(raw)
            inches = round((raw - feet) * 10)
            height_cm = round(feet * 30.48 + inches * 2.54, 1)
        else:
            height_cm = raw
        if not (100 <= height_cm <= 250):
            raise ValueError
    except ValueError:
        await message.answer(t("onboarding_height_invalid", lang))
        return

    user_service = UserService(session)
    updated = await user_service.update_user(db_user.telegram_id, height=height_cm)
    await state.clear()
    await message.answer(
        t("profile_updated", lang) + "\n\n" + _build_profile_text(updated, lang),
        reply_markup=profile_keyboard(lang),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "profile:edit:weight")
async def cb_edit_weight(callback: CallbackQuery, state: FSMContext, db_user: User, lang: str):
    await state.set_state(ProfileEditStates.editing_weight)
    key = "onboarding_weight_ask" if db_user.units == "metric" else "onboarding_weight_ask_imperial"
    await callback.message.edit_text(t(key, lang), parse_mode="HTML")
    await callback.answer()


@router.message(ProfileEditStates.editing_weight)
async def process_edit_weight(message: Message, state: FSMContext, db_user: User, lang: str, session: AsyncSession):
    try:
        raw = float(message.text.strip().replace(",", "."))
        if db_user.units == "imperial":
            weight_kg = round(raw / 2.20462, 1)
        else:
            weight_kg = raw
        if not (30 <= weight_kg <= 300):
            raise ValueError
    except ValueError:
        await message.answer(t("onboarding_weight_invalid", lang))
        return

    user_service = UserService(session)
    updated = await user_service.update_user(db_user.telegram_id, weight=weight_kg)
    await state.clear()
    await message.answer(
        t("profile_updated", lang) + "\n\n" + _build_profile_text(updated, lang),
        reply_markup=profile_keyboard(lang),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "profile:edit:goal")
async def cb_edit_goal(callback: CallbackQuery, lang: str):
    await callback.message.edit_text(
        t("onboarding_goal_ask", lang),
        reply_markup=goal_edit_keyboard(lang),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("profile:set:goal:"))
async def cb_set_goal(callback: CallbackQuery, db_user: User, lang: str, session: AsyncSession):
    goal = callback.data.split(":")[-1]
    user_service = UserService(session)
    updated = await user_service.update_user(db_user.telegram_id, goal=goal)
    await callback.message.edit_text(
        t("profile_updated", lang) + "\n\n" + _build_profile_text(updated, lang),
        reply_markup=profile_keyboard(lang),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "profile:recalc")
async def cb_recalc_calories(callback: CallbackQuery, db_user: User, lang: str, session: AsyncSession):
    user_service = UserService(session)
    calories = await user_service.recalculate_calories(db_user)
    if calories:
        await callback.answer(
            t("calories_recalculated", lang, calories=int(calories)),
            show_alert=True,
        )
        updated = await user_service.get_by_telegram_id(db_user.telegram_id)
        await callback.message.edit_text(
            _build_profile_text(updated, lang),
            reply_markup=profile_keyboard(lang),
            parse_mode="HTML",
        )
    else:
        await callback.answer(t("error_general", lang), show_alert=True)
