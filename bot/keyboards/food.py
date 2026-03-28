from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.locales import t


def food_result_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=t("btn_save_entry", lang), callback_data="food:save"),
            InlineKeyboardButton(text=t("btn_edit_grams", lang), callback_data="food:edit_grams"),
        ],
        [
            InlineKeyboardButton(text=t("btn_back", lang), callback_data="menu:main"),
        ],
    ])


def food_saved_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=t("btn_diary", lang), callback_data="menu:diary"),
            InlineKeyboardButton(text=t("btn_profile", lang), callback_data="menu:profile"),
        ],
        [
            InlineKeyboardButton(text=t("btn_settings", lang), callback_data="menu:settings"),
        ],
    ])
