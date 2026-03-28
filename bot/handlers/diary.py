import logging
from datetime import date

from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards.diary import diary_keyboard
from bot.keyboards.main_menu import main_menu_keyboard
from bot.locales import t
from bot.models.user import User
from bot.services.diary_service import DiaryService

logger = logging.getLogger(__name__)
router = Router()


@router.callback_query(F.data == "diary:today")
async def cb_diary_today(callback: CallbackQuery, db_user: User, lang: str, session: AsyncSession):
    diary_service = DiaryService(session)
    entries = await diary_service.get_today_entries(db_user.telegram_id)

    if not entries:
        await callback.message.edit_text(
            t("diary_empty", lang),
            reply_markup=diary_keyboard(lang),
            parse_mode="HTML",
        )
        await callback.answer()
        return

    # Build entries text
    entries_text = ""
    total_cal = 0.0
    total_prot = 0.0
    total_fat = 0.0
    total_carbs = 0.0

    for entry in entries:
        time_str = entry.eaten_at.strftime("%H:%M")
        entries_text += t(
            "diary_entry_line",
            lang,
            time=time_str,
            dish=entry.dish_name[:30],
            calories=round(entry.calories),
        )
        total_cal += entry.calories
        total_prot += entry.protein
        total_fat += entry.fat
        total_carbs += entry.carbs

    remaining = (db_user.daily_calories or 0) - total_cal
    today_str = date.today().strftime("%d.%m.%Y")

    text = t(
        "diary_today",
        lang,
        date=today_str,
        entries=entries_text,
        total_cal=round(total_cal),
        total_prot=round(total_prot, 1),
        total_fat=round(total_fat, 1),
        total_carbs=round(total_carbs, 1),
        remaining=round(remaining),
    )

    if not db_user.daily_calories:
        text += t("diary_no_norm", lang)

    await callback.message.edit_text(
        text,
        reply_markup=diary_keyboard(lang),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "diary:week")
async def cb_diary_week(callback: CallbackQuery, db_user: User, lang: str, session: AsyncSession):
    diary_service = DiaryService(session)
    entries = await diary_service.get_week_entries(db_user.telegram_id)

    if not entries:
        await callback.message.edit_text(
            t("diary_empty", lang),
            reply_markup=diary_keyboard(lang),
            parse_mode="HTML",
        )
        await callback.answer()
        return

    # Group by day
    from collections import defaultdict
    days: dict = defaultdict(list)
    for entry in entries:
        day_key = entry.eaten_at.strftime("%d.%m")
        days[day_key].append(entry)

    entries_text = ""
    total_cal = 0.0

    for day, day_entries in sorted(days.items()):
        entries_text += t("diary_day_header", lang, date=day)
        for entry in day_entries:
            time_str = entry.eaten_at.strftime("%H:%M")
            entries_text += t(
                "diary_entry_line",
                lang,
                time=time_str,
                dish=entry.dish_name[:30],
                calories=round(entry.calories),
            )
            total_cal += entry.calories

    text = t(
        "diary_week",
        lang,
        entries=entries_text,
        total_cal=round(total_cal),
    )

    await callback.message.edit_text(
        text,
        reply_markup=diary_keyboard(lang),
        parse_mode="HTML",
    )
    await callback.answer()
