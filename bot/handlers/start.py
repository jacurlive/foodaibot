import logging

from aiogram import Router, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

from bot.config import settings
from bot.keyboards.onboarding import language_keyboard
from bot.locales import t
from bot.models.user import User

logger = logging.getLogger(__name__)
router = Router()


def open_app_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=t("btn_open_app", lang),
            web_app=WebAppInfo(url=settings.WEBAPP_URL),
        )]
    ])


@router.message(CommandStart())
async def cmd_start(message: Message, bot: Bot, db_user: User, lang: str):
    if db_user.is_onboarded:
        await message.answer(
            t("welcome_back", lang),
            reply_markup=open_app_keyboard(lang),
            parse_mode="HTML",
        )
    else:
        await message.answer(
            t("welcome", lang),
            reply_markup=language_keyboard(),
            parse_mode="HTML",
        )

    # Notify admins
    username = f"@{message.from_user.username}" if message.from_user.username else "—"
    name = db_user.name or message.from_user.first_name or "—"
    status = "повторный" if db_user.is_onboarded else "новый"
    notify_text = (
        f"👤 <b>Старт бота</b> ({status})\n"
        f"ID: <code>{message.from_user.id}</code>\n"
        f"Username: {username}\n"
        f"Имя: {name}"
    )
    for admin_id in settings.get_admin_ids():
        try:
            await bot.send_message(admin_id, notify_text, parse_mode="HTML")
        except Exception:
            pass
