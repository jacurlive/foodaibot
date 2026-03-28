from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, func
from datetime import datetime, date, timedelta
from typing import Optional

from bot.models.food_entry import FoodEntry


class DiaryService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_entry(
        self,
        user_id: int,
        dish_name: str,
        calories: float,
        protein: float,
        fat: float,
        carbs: float,
        description: Optional[str] = None,
        photo_file_id: Optional[str] = None,
    ) -> FoodEntry:
        entry = FoodEntry(
            user_id=user_id,
            dish_name=dish_name,
            calories=calories,
            protein=protein,
            fat=fat,
            carbs=carbs,
            description=description,
            photo_file_id=photo_file_id,
        )
        self.session.add(entry)
        await self.session.commit()
        await self.session.refresh(entry)
        return entry

    async def get_today_entries(self, user_id: int) -> list[FoodEntry]:
        today = date.today()
        start = datetime.combine(today, datetime.min.time())
        end = datetime.combine(today, datetime.max.time())
        result = await self.session.execute(
            select(FoodEntry)
            .where(
                FoodEntry.user_id == user_id,
                FoodEntry.eaten_at >= start,
                FoodEntry.eaten_at <= end,
            )
            .order_by(FoodEntry.eaten_at.asc())
        )
        return result.scalars().all()

    async def get_week_entries(self, user_id: int) -> list[FoodEntry]:
        today = date.today()
        week_start = today - timedelta(days=today.weekday())
        start = datetime.combine(week_start, datetime.min.time())
        result = await self.session.execute(
            select(FoodEntry)
            .where(
                FoodEntry.user_id == user_id,
                FoodEntry.eaten_at >= start,
            )
            .order_by(FoodEntry.eaten_at.asc())
        )
        return result.scalars().all()

    async def get_all_entries(
        self, user_id: int, offset: int = 0, limit: int = 5
    ) -> tuple[list[FoodEntry], int]:
        total_result = await self.session.execute(
            select(func.count(FoodEntry.id)).where(FoodEntry.user_id == user_id)
        )
        total = total_result.scalar_one()

        result = await self.session.execute(
            select(FoodEntry)
            .where(FoodEntry.user_id == user_id)
            .order_by(FoodEntry.eaten_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return result.scalars().all(), total

    async def delete_entry(self, entry_id: int, user_id: int) -> bool:
        result = await self.session.execute(
            delete(FoodEntry).where(
                FoodEntry.id == entry_id,
                FoodEntry.user_id == user_id,
            )
        )
        await self.session.commit()
        return result.rowcount > 0

    async def get_entry_by_id(self, entry_id: int) -> Optional[FoodEntry]:
        result = await self.session.execute(
            select(FoodEntry).where(FoodEntry.id == entry_id)
        )
        return result.scalar_one_or_none()
