from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.locales import t


def admin_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t("btn_admin_broadcast", lang), callback_data="admin:broadcast")],
        [InlineKeyboardButton(text=t("btn_admin_top_users", lang), callback_data="admin:top_users")],
        [InlineKeyboardButton(text=t("btn_admin_ban", lang), callback_data="admin:ban")],
        [InlineKeyboardButton(text=t("btn_back", lang), callback_data="menu:main")],
    ])


def broadcast_confirm_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=t("btn_yes", lang), callback_data="admin:broadcast:confirm"),
            InlineKeyboardButton(text=t("btn_no", lang), callback_data="admin:broadcast:cancel"),
        ],
    ])
