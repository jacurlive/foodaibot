from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from typing import Optional

from bot.models.user import User


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        result = await self.session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        return result.scalar_one_or_none()

    async def get_or_create(
        self,
        telegram_id: int,
        username: Optional[str] = None,
        first_name: Optional[str] = None,
    ) -> tuple[User, bool]:
        user = await self.get_by_telegram_id(telegram_id)
        if user:
            # Update username/first_name if changed
            changed = False
            if username and user.username != username:
                user.username = username
                changed = True
            if first_name and user.first_name != first_name:
                user.first_name = first_name
                changed = True
            if changed:
                await self.session.commit()
                await self.session.refresh(user)
            return user, False

        user = User(
            telegram_id=telegram_id,
            username=username,
            first_name=first_name,
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user, True

    async def update_user(self, telegram_id: int, **kwargs) -> Optional[User]:
        user = await self.get_by_telegram_id(telegram_id)
        if not user:
            return None
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def complete_onboarding(self, user: User) -> User:
        user.is_onboarded = True
        calories = user.calculate_daily_calories()
        user.daily_calories = calories
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def recalculate_calories(self, user: User) -> float | None:
        calories = user.calculate_daily_calories()
        user.daily_calories = calories
        await self.session.commit()
        return calories
