from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.locales import t, LANGUAGE_NAMES


def language_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=LANGUAGE_NAMES["ru"], callback_data="lang:ru")],
        [InlineKeyboardButton(text=LANGUAGE_NAMES["en"], callback_data="lang:en")],
        [InlineKeyboardButton(text=LANGUAGE_NAMES["uz"], callback_data="lang:uz")],
    ])


def gender_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=t("btn_gender_male", lang), callback_data="gender:male"),
            InlineKeyboardButton(text=t("btn_gender_female", lang), callback_data="gender:female"),
        ],
    ])


def goal_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t("btn_goal_lose", lang), callback_data="goal:lose")],
        [InlineKeyboardButton(text=t("btn_goal_maintain", lang), callback_data="goal:maintain")],
        [InlineKeyboardButton(text=t("btn_goal_gain", lang), callback_data="goal:gain")],
    ])


def units_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t("btn_units_metric", lang), callback_data="units:metric")],
        [InlineKeyboardButton(text=t("btn_units_imperial", lang), callback_data="units:imperial")],
    ])
