from typing import AsyncGenerator, Optional
from fastapi import Depends, Header, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from bot.database import session_pool
from bot.models.user import User


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_pool() as session:
        yield session


async def get_current_user(
    session: AsyncSession = Depends(get_session),
    x_telegram_user_id: Optional[int] = Header(None, alias="X-Telegram-User-Id"),
    user_id: Optional[int] = Query(None),
) -> User:
    telegram_id = x_telegram_user_id or user_id
    if not telegram_id:
        raise HTTPException(status_code=401, detail="User ID required")

    result = await session.execute(
        select(User).where(User.telegram_id == telegram_id)
    )
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
