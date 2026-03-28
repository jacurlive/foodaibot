import logging
import asyncio

from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards.admin import admin_keyboard, broadcast_confirm_keyboard
from bot.keyboards.main_menu import main_menu_keyboard
from bot.locales import t
from bot.models.user import User
from bot.services.admin_service import AdminService
from bot.config import settings

logger = logging.getLogger(__name__)
router = Router()


class AdminStates(StatesGroup):
    broadcast_input = State()
    broadcast_confirm = State()
    ban_input = State()


def is_admin(user: User) -> bool:
    return user.telegram_id in settings.get_admin_ids() or user.is_admin


@router.message(Command("admin"))
async def cmd_admin(message: Message, db_user: User, lang: str, session: AsyncSession):
    if not is_admin(db_user):
        await message.answer(t("not_admin", lang), parse_mode="HTML")
        return

    admin_service = AdminService(session)
    stats = await admin_service.get_stats()

    await message.answer(
        t("admin_panel", lang, **stats),
        reply_markup=admin_keyboard(lang),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "menu:admin")
async def cb_admin_panel(callback: CallbackQuery, db_user: User, lang: str, session: AsyncSession):
    if not is_admin(db_user):
        await callback.answer(t("not_admin", lang), show_alert=True)
        return

    admin_service = AdminService(session)
    stats = await admin_service.get_stats()

    await callback.message.edit_text(
        t("admin_panel", lang, **stats),
        reply_markup=admin_keyboard(lang),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "admin:top_users")
async def cb_top_users(callback: CallbackQuery, db_user: User, lang: str, session: AsyncSession):
    if not is_admin(db_user):
        await callback.answer(t("not_admin", lang), show_alert=True)
        return

    admin_service = AdminService(session)
    top = await admin_service.get_top_users(limit=10)

    users_text = ""
    for rank, (user, count) in enumerate(top, start=1):
        name = user.name or user.username or f"id:{user.telegram_id}"
        users_text += t("admin_top_user_line", lang, rank=rank, name=name, count=count)

    await callback.message.edit_text(
        t("admin_top_users", lang, users=users_text or "—"),
        reply_markup=admin_keyboard(lang),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "admin:broadcast")
async def cb_broadcast_start(callback: CallbackQuery, db_user: User, lang: str, state: FSMContext):
    if not is_admin(db_user):
        await callback.answer(t("not_admin", lang), show_alert=True)
        return

    await state.set_state(AdminStates.broadcast_input)
    await callback.message.edit_text(
        t("admin_broadcast_ask", lang),
        parse_mode="HTML",
    )
    await callback.answer()


@router.message(AdminStates.broadcast_input)
async def process_broadcast_input(message: Message, state: FSMContext, db_user: User, lang: str, session: AsyncSession):
    if not is_admin(db_user):
        return

    broadcast_text = message.text
    admin_service = AdminService(session)
    users = await admin_service.get_all_users()

    await state.update_data(broadcast_text=broadcast_text, user_count=len(users))
    await state.set_state(AdminStates.broadcast_confirm)

    await message.answer(
        t("admin_broadcast_confirm", lang, count=len(users), text=broadcast_text),
        reply_markup=broadcast_confirm_keyboard(lang),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "admin:broadcast:confirm")
async def cb_broadcast_confirm(
    callback: CallbackQuery, state: FSMContext, db_user: User, lang: str, bot: Bot, session: AsyncSession
):
    if not is_admin(db_user):
        await callback.answer(t("not_admin", lang), show_alert=True)
        return

    data = await state.get_data()
    broadcast_text = data.get("broadcast_text", "")
    await state.clear()

    admin_service = AdminService(session)
    users = await admin_service.get_all_users()

    sent = 0
    for user in users:
        try:
            await bot.send_message(user.telegram_id, broadcast_text, parse_mode="HTML")
            sent += 1
            await asyncio.sleep(0.05)  # Rate limit
        except Exception as e:
            logger.warning(f"Failed to send broadcast to {user.telegram_id}: {e}")

    await callback.message.edit_text(
        t("admin_broadcast_done", lang, sent=sent),
        reply_markup=admin_keyboard(lang),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "admin:broadcast:cancel")
async def cb_broadcast_cancel(callback: CallbackQuery, state: FSMContext, db_user: User, lang: str, session: AsyncSession):
    await state.clear()
    admin_service = AdminService(session)
    stats = await admin_service.get_stats()
    await callback.message.edit_text(
        t("admin_panel", lang, **stats),
        reply_markup=admin_keyboard(lang),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "admin:ban")
async def cb_ban_start(callback: CallbackQuery, db_user: User, lang: str, state: FSMContext):
    if not is_admin(db_user):
        await callback.answer(t("not_admin", lang), show_alert=True)
        return

    await state.set_state(AdminStates.ban_input)
    await callback.message.edit_text(
        t("admin_ban_ask", lang),
        parse_mode="HTML",
    )
    await callback.answer()


@router.message(AdminStates.ban_input)
async def process_ban_input(message: Message, state: FSMContext, db_user: User, lang: str, session: AsyncSession):
    if not is_admin(db_user):
        return

    try:
        target_id = int(message.text.strip())
    except ValueError:
        await message.answer(t("error_invalid_input", lang))
        return

    admin_service = AdminService(session)
    result = await admin_service.toggle_ban(target_id)
    await state.clear()

    if not result:
        await message.answer(
            t("admin_user_not_found", lang),
            reply_markup=admin_keyboard(lang),
            parse_mode="HTML",
        )
        return

    user, is_banned = result
    msg_key = "admin_ban_done" if is_banned else "admin_unban_done"
    await message.answer(
        t(msg_key, lang, user_id=target_id),
        reply_markup=admin_keyboard(lang),
        parse_mode="HTML",
    )
