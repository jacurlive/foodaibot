from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.keyboards.diary import diary_keyboard
from bot.keyboards.settings import settings_keyboard
from bot.locales import t
from bot.models.user import User

router = Router()


@router.callback_query(F.data == "menu:diary")
async def cb_diary_menu(callback: CallbackQuery, db_user: User, lang: str):
    await callback.message.edit_text(
        t("diary_title", lang),
        reply_markup=diary_keyboard(lang),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "menu:settings")
async def cb_settings_menu(callback: CallbackQuery, db_user: User, lang: str):
    await callback.message.edit_text(
        t("settings_title", lang),
        reply_markup=settings_keyboard(lang),
        parse_mode="HTML",
    )
    await callback.answer()
