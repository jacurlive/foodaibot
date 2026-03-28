from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.locales import t


def profile_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=t("btn_edit_name", lang), callback_data="profile:edit:name"),
            InlineKeyboardButton(text=t("btn_edit_age", lang), callback_data="profile:edit:age"),
        ],
        [
            InlineKeyboardButton(text=t("btn_edit_gender", lang), callback_data="profile:edit:gender"),
            InlineKeyboardButton(text=t("btn_edit_weight", lang), callback_data="profile:edit:weight"),
        ],
        [
            InlineKeyboardButton(text=t("btn_edit_height", lang), callback_data="profile:edit:height"),
            InlineKeyboardButton(text=t("btn_edit_goal", lang), callback_data="profile:edit:goal"),
        ],
        [InlineKeyboardButton(text=t("btn_recalc_calories", lang), callback_data="profile:recalc")],
        [InlineKeyboardButton(text=t("btn_back", lang), callback_data="menu:main")],
    ])


def gender_edit_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=t("btn_gender_male", lang), callback_data="profile:set:gender:male"),
            InlineKeyboardButton(text=t("btn_gender_female", lang), callback_data="profile:set:gender:female"),
        ],
        [InlineKeyboardButton(text=t("btn_back", lang), callback_data="menu:profile")],
    ])


def goal_edit_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t("btn_goal_lose", lang), callback_data="profile:set:goal:lose")],
        [InlineKeyboardButton(text=t("btn_goal_maintain", lang), callback_data="profile:set:goal:maintain")],
        [InlineKeyboardButton(text=t("btn_goal_gain", lang), callback_data="profile:set:goal:gain")],
        [InlineKeyboardButton(text=t("btn_back", lang), callback_data="menu:profile")],
    ])
