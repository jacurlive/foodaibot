from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.locales import t


def diary_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=t("btn_diary_today", lang), callback_data="diary:today"),
            InlineKeyboardButton(text=t("btn_diary_week", lang), callback_data="diary:week"),
        ],
        [InlineKeyboardButton(text=t("btn_back", lang), callback_data="menu:main")],
    ])
