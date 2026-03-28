import logging
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.locales import t
from bot.services.user_service import UserService

logger = logging.getLogger(__name__)


class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        user_obj = None

        if isinstance(event, Message):
            user_obj = event.from_user
        elif isinstance(event, CallbackQuery):
            user_obj = event.from_user

        if not user_obj:
            return await handler(event, data)

        session: AsyncSession = data.get("session")
        if not session:
            return await handler(event, data)

        user_service = UserService(session)
        db_user, _ = await user_service.get_or_create(
            telegram_id=user_obj.id,
            username=user_obj.username,
            first_name=user_obj.first_name,
        )

        if db_user.is_banned:
            lang = db_user.language or "en"
            if isinstance(event, Message):
                await event.answer(t("error_banned", lang))
            elif isinstance(event, CallbackQuery):
                await event.answer(t("error_banned", lang), show_alert=True)
            return

        data["db_user"] = db_user
        data["lang"] = db_user.language or "en"
        return await handler(event, data)
