import logging

from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards.settings import (
    settings_keyboard,
    settings_language_keyboard,
    settings_units_keyboard,
    notifications_keyboard,
)
from bot.keyboards.main_menu import main_menu_keyboard
from bot.locales import t, LANGUAGE_NAMES
from bot.models.user import User
from bot.services.user_service import UserService

logger = logging.getLogger(__name__)
router = Router()


@router.callback_query(F.data == "settings:language")
async def cb_settings_language(callback: CallbackQuery, db_user: User, lang: str):
    await callback.message.edit_text(
        t("settings_language", lang),
        reply_markup=settings_language_keyboard(lang),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("setlang:"))
async def cb_set_language(callback: CallbackQuery, db_user: User, session: AsyncSession):
    new_lang = callback.data.split(":")[1]
    user_service = UserService(session)
    await user_service.update_user(db_user.telegram_id, language=new_lang)

    await callback.message.edit_text(
        t("settings_language_changed", new_lang),
        reply_markup=settings_keyboard(new_lang),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "settings:units")
async def cb_settings_units(callback: CallbackQuery, db_user: User, lang: str):
    units_label = t("units_metric" if db_user.units == "metric" else "units_imperial", lang)
    await callback.message.edit_text(
        t("settings_units", lang, units=units_label),
        reply_markup=settings_units_keyboard(lang, db_user.units),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("setunits:"))
async def cb_set_units(callback: CallbackQuery, db_user: User, lang: str, session: AsyncSession):
    new_units = callback.data.split(":")[1]
    user_service = UserService(session)
    await user_service.update_user(db_user.telegram_id, units=new_units)
    db_user.units = new_units

    units_label = t("units_metric" if new_units == "metric" else "units_imperial", lang)
    await callback.message.edit_text(
        t("settings_units_changed", lang, units=units_label),
        reply_markup=settings_units_keyboard(lang, new_units),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "settings:notifications")
async def cb_notifications(callback: CallbackQuery, db_user: User, lang: str):
    await callback.message.edit_text(
        t("notifications_title", lang),
        reply_markup=notifications_keyboard(lang, db_user),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("notify:"))
async def cb_toggle_notify(callback: CallbackQuery, db_user: User, lang: str, session: AsyncSession):
    period = callback.data.split(":")[1]
    user_service = UserService(session)

    field_map = {
        "morning": "notify_morning",
        "afternoon": "notify_afternoon",
        "evening": "notify_evening",
    }
    field = field_map.get(period)
    if not field:
        await callback.answer(t("error_general", lang))
        return

    current = getattr(db_user, field)
    updated = await user_service.update_user(db_user.telegram_id, **{field: not current})

    await callback.message.edit_text(
        t("notifications_title", lang),
        reply_markup=notifications_keyboard(lang, updated),
        parse_mode="HTML",
    )
    await callback.answer(t("notify_updated", lang))
