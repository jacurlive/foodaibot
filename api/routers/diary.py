from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date, datetime, timedelta
from typing import List

from api.dependencies import get_session, get_current_user
from api.schemas import (
    DiaryTodaySchema,
    DiaryWeekSchema,
    DiaryHistorySchema,
    DeleteResponseSchema,
    FoodEntrySchema,
    MacroTotals,
    DiaryDaySchema,
)
from bot.models.user import User
from bot.services.diary_service import DiaryService

router = APIRouter(prefix="/diary", tags=["diary"])


def calc_totals(entries) -> MacroTotals:
    return MacroTotals(
        calories=round(sum(e.calories for e in entries), 1),
        protein=round(sum(e.protein for e in entries), 1),
        fat=round(sum(e.fat for e in entries), 1),
        carbs=round(sum(e.carbs for e in entries), 1),
    )


@router.get("/today", response_model=DiaryTodaySchema)
async def get_today(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    service = DiaryService(session)
    entries = await service.get_today_entries(current_user.telegram_id)
    totals = calc_totals(entries)
    goal = current_user.daily_calories or 2000.0
    remaining = max(0.0, goal - totals.calories)

    return DiaryTodaySchema(
        date=date.today().isoformat(),
        entries=[FoodEntrySchema.model_validate(e) for e in entries],
        totals=totals,
        remaining_calories=round(remaining, 1),
    )


@router.get("/week", response_model=DiaryWeekSchema)
async def get_week(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    service = DiaryService(session)
    entries = await service.get_week_entries(current_user.telegram_id)

    # Group by date
    days_map: dict[str, list] = {}
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    for i in range(7):
        d = (week_start + timedelta(days=i)).isoformat()
        days_map[d] = []

    for entry in entries:
        d = entry.eaten_at.date().isoformat()
        if d in days_map:
            days_map[d].append(entry)

    days = []
    for d, day_entries in days_map.items():
        days.append(
            DiaryDaySchema(
                date=d,
                entries=[FoodEntrySchema.model_validate(e) for e in day_entries],
                totals=calc_totals(day_entries),
            )
        )

    return DiaryWeekSchema(days=days)


@router.get("/history", response_model=DiaryHistorySchema)
async def get_history(
    page: int = 1,
    limit: int = 20,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    service = DiaryService(session)
    offset = (page - 1) * limit
    entries, total = await service.get_all_entries(
        current_user.telegram_id, offset=offset, limit=limit
    )
    pages = max(1, (total + limit - 1) // limit)

    return DiaryHistorySchema(
        entries=[FoodEntrySchema.model_validate(e) for e in entries],
        total=total,
        page=page,
        pages=pages,
    )


@router.delete("/entry/{entry_id}", response_model=DeleteResponseSchema)
async def delete_entry(
    entry_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    service = DiaryService(session)
    ok = await service.delete_entry(entry_id, current_user.telegram_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Entry not found")
    return DeleteResponseSchema(ok=True)
