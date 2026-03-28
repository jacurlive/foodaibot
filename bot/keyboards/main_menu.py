from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.locales import t


def main_menu_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=t("btn_diary", lang), callback_data="menu:diary"),
            InlineKeyboardButton(text=t("btn_profile", lang), callback_data="menu:profile"),
        ],
        [
            InlineKeyboardButton(text=t("btn_settings", lang), callback_data="menu:settings"),
        ],
    ])
