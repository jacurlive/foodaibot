from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.locales import t, LANGUAGE_NAMES
from bot.models.user import User


def settings_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t("btn_change_language", lang), callback_data="settings:language")],
        [InlineKeyboardButton(text=t("btn_change_units", lang), callback_data="settings:units")],
        [InlineKeyboardButton(text=t("btn_notifications", lang), callback_data="settings:notifications")],
        [InlineKeyboardButton(text=t("btn_back", lang), callback_data="menu:main")],
    ])


def settings_language_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=LANGUAGE_NAMES["ru"], callback_data="setlang:ru")],
        [InlineKeyboardButton(text=LANGUAGE_NAMES["en"], callback_data="setlang:en")],
        [InlineKeyboardButton(text=LANGUAGE_NAMES["uz"], callback_data="setlang:uz")],
        [InlineKeyboardButton(text=t("btn_back", lang), callback_data="menu:settings")],
    ])


def settings_units_keyboard(lang: str, current: str) -> InlineKeyboardMarkup:
    metric_check = "✅ " if current == "metric" else ""
    imperial_check = "✅ " if current == "imperial" else ""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=f"{metric_check}{t('btn_units_metric', lang)}",
            callback_data="setunits:metric",
        )],
        [InlineKeyboardButton(
            text=f"{imperial_check}{t('btn_units_imperial', lang)}",
            callback_data="setunits:imperial",
        )],
        [InlineKeyboardButton(text=t("btn_back", lang), callback_data="menu:settings")],
    ])


def notifications_keyboard(lang: str, user: User) -> InlineKeyboardMarkup:
    def status(flag: bool) -> str:
        return t("notify_on", lang) if flag else t("notify_off", lang)

    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=f"{t('btn_notify_morning', lang)} {status(user.notify_morning)}",
            callback_data="notify:morning",
        )],
        [InlineKeyboardButton(
            text=f"{t('btn_notify_afternoon', lang)} {status(user.notify_afternoon)}",
            callback_data="notify:afternoon",
        )],
        [InlineKeyboardButton(
            text=f"{t('btn_notify_evening', lang)} {status(user.notify_evening)}",
            callback_data="notify:evening",
        )],
        [InlineKeyboardButton(text=t("btn_back", lang), callback_data="menu:settings")],
    ])
