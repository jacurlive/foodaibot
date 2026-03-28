import logging
import math

from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards.history import history_keyboard
from bot.keyboards.main_menu import main_menu_keyboard
from bot.locales import t
from bot.models.user import User
from bot.services.diary_service import DiaryService

logger = logging.getLogger(__name__)
router = Router()

PAGE_SIZE = 5


async def _show_history(callback: CallbackQuery, db_user: User, lang: str, session: AsyncSession, page: int = 1):
    diary_service = DiaryService(session)
    offset = (page - 1) * PAGE_SIZE
    entries, total = await diary_service.get_all_entries(db_user.telegram_id, offset=offset, limit=PAGE_SIZE)

    if total == 0:
        await callback.message.edit_text(
            t("history_empty", lang),
            reply_markup=main_menu_keyboard(lang),
            parse_mode="HTML",
        )
        await callback.answer()
        return

    total_pages = max(1, math.ceil(total / PAGE_SIZE))

    text = t("history_title", lang) + "\n\n"
    for entry in entries:
        date_str = entry.eaten_at.strftime("%d.%m.%Y %H:%M")
        text += t(
            "history_entry",
            lang,
            dish=entry.dish_name,
            date=date_str,
            calories=round(entry.calories),
            protein=round(entry.protein, 1),
            fat=round(entry.fat, 1),
            carbs=round(entry.carbs, 1),
        ) + "\n\n"

    text += f"\n{t('history_page', lang, page=page, total=total_pages)}"

    await callback.message.edit_text(
        text,
        reply_markup=history_keyboard(entries, lang, page, total_pages),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "menu:history")
async def cb_history(callback: CallbackQuery, db_user: User, lang: str, session: AsyncSession):
    await _show_history(callback, db_user, lang, session, page=1)


@router.callback_query(F.data.startswith("history:page:"))
async def cb_history_page(callback: CallbackQuery, db_user: User, lang: str, session: AsyncSession):
    page = int(callback.data.split(":")[-1])
    await _show_history(callback, db_user, lang, session, page=page)


@router.callback_query(F.data.startswith("history:delete:"))
async def cb_delete_entry(callback: CallbackQuery, db_user: User, lang: str, session: AsyncSession):
    entry_id = int(callback.data.split(":")[-1])
    diary_service = DiaryService(session)
    deleted = await diary_service.delete_entry(entry_id, db_user.telegram_id)

    if deleted:
        await callback.answer(t("entry_deleted", lang), show_alert=False)
    else:
        await callback.answer(t("error_general", lang), show_alert=True)
        return

    # Refresh history view
    await _show_history(callback, db_user, lang, session, page=1)
