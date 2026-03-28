from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update
from datetime import datetime, date, timedelta
from typing import Optional

from bot.models.user import User
from bot.models.food_entry import FoodEntry


class AdminService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_stats(self) -> dict:
        today = datetime.combine(date.today(), datetime.min.time())
        week_start = today - timedelta(days=date.today().weekday())
        month_start = today.replace(day=1)

        total_users = await self.session.scalar(select(func.count(User.id)))

        today_users = await self.session.scalar(
            select(func.count(User.id)).where(User.created_at >= today)
        )

        week_users = await self.session.scalar(
            select(func.count(User.id)).where(User.created_at >= week_start)
        )

        month_users = await self.session.scalar(
            select(func.count(User.id)).where(User.created_at >= month_start)
        )

        total_analyses = await self.session.scalar(
            select(func.count(FoodEntry.id))
        )

        return {
            "total_users": total_users or 0,
            "today": today_users or 0,
            "week": week_users or 0,
            "month": month_users or 0,
            "total_analyses": total_analyses or 0,
        }

    async def get_top_users(self, limit: int = 10) -> list[tuple[User, int]]:
        result = await self.session.execute(
            select(User, func.count(FoodEntry.id).label("count"))
            .join(FoodEntry, FoodEntry.user_id == User.telegram_id, isouter=True)
            .group_by(User.id)
            .order_by(func.count(FoodEntry.id).desc())
            .limit(limit)
        )
        return result.all()

    async def get_all_users(self) -> list[User]:
        result = await self.session.execute(
            select(User).where(User.is_banned == False)
        )
        return result.scalars().all()

    async def ban_user(self, telegram_id: int) -> Optional[User]:
        user = await self.session.scalar(
            select(User).where(User.telegram_id == telegram_id)
        )
        if not user:
            return None
        user.is_banned = True
        await self.session.commit()
        return user

    async def unban_user(self, telegram_id: int) -> Optional[User]:
        user = await self.session.scalar(
            select(User).where(User.telegram_id == telegram_id)
        )
        if not user:
            return None
        user.is_banned = False
        await self.session.commit()
        return user

    async def toggle_ban(self, telegram_id: int) -> Optional[tuple[User, bool]]:
        """Returns (user, is_now_banned)"""
        user = await self.session.scalar(
            select(User).where(User.telegram_id == telegram_id)
        )
        if not user:
            return None
        user.is_banned = not user.is_banned
        await self.session.commit()
        await self.session.refresh(user)
        return user, user.is_banned
