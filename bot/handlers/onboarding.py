import logging

from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from sqlalchemy.ext.asyncio import AsyncSession

from bot.config import settings
from bot.locales import t
from bot.models.user import User
from bot.services.user_service import UserService

logger = logging.getLogger(__name__)
router = Router()


def open_app_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=t("btn_open_app", lang),
            web_app=WebAppInfo(url=settings.WEBAPP_URL),
        )]
    ])


@router.callback_query(F.data.startswith("lang:"))
async def cb_select_language(
    callback: CallbackQuery,
    db_user: User,
    session: AsyncSession,
):
    lang = callback.data.split(":")[1]
    user_service = UserService(session)
    await user_service.update_user(db_user.telegram_id, language=lang)

    await callback.message.edit_text(
        t("welcome_open_app", lang),
        reply_markup=open_app_keyboard(lang),
        parse_mode="HTML",
    )
    await callback.answer()
