from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import date, datetime, timedelta
from collections import defaultdict

from api.dependencies import get_session, get_current_user
from api.schemas import StatsOverviewSchema, CalorieDaySchema, MacroAvgSchema
from bot.models.user import User
from bot.models.food_entry import FoodEntry

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("/overview", response_model=StatsOverviewSchema)
async def get_overview(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    today = date.today()

    # All entries ever
    all_result = await session.execute(
        select(FoodEntry)
        .where(FoodEntry.user_id == current_user.telegram_id)
        .order_by(FoodEntry.eaten_at.asc())
    )
    all_entries = all_result.scalars().all()

    total_entries = len(all_entries)
    total_calories_consumed = round(sum(e.calories for e in all_entries), 1)

    # Group by date
    day_calories: dict[str, float] = defaultdict(float)
    day_entries_count: dict[str, int] = defaultdict(int)
    for e in all_entries:
        d = e.eaten_at.date().isoformat()
        day_calories[d] += e.calories
        day_entries_count[d] += 1

    unique_days = len(day_calories)
    avg_calories_per_day = round(total_calories_consumed / unique_days, 1) if unique_days > 0 else 0.0

    # Streak calculation
    streak_days = 0
    check_date = today
    while check_date.isoformat() in day_calories:
        streak_days += 1
        check_date -= timedelta(days=1)

    # Best day (most entries)
    best_day = None
    if day_entries_count:
        best_day = max(day_entries_count, key=lambda d: day_entries_count[d])

    # Today stats
    today_str = today.isoformat()
    today_calories = round(day_calories.get(today_str, 0.0), 1)
    today_goal = current_user.daily_calories or 2000.0
    today_percent = round((today_calories / today_goal) * 100, 1) if today_goal > 0 else 0.0

    # Weekly calories (last 7 days)
    weekly_calories = []
    for i in range(6, -1, -1):
        d = (today - timedelta(days=i)).isoformat()
        weekly_calories.append(
            CalorieDaySchema(date=d, calories=round(day_calories.get(d, 0.0), 1))
        )

    # Monthly calories (last 30 days)
    monthly_calories = []
    for i in range(29, -1, -1):
        d = (today - timedelta(days=i)).isoformat()
        monthly_calories.append(
            CalorieDaySchema(date=d, calories=round(day_calories.get(d, 0.0), 1))
        )

    # Week macro totals/averages
    week_start = today - timedelta(days=6)
    week_start_dt = datetime.combine(week_start, datetime.min.time())
    week_entries_result = await session.execute(
        select(FoodEntry).where(
            FoodEntry.user_id == current_user.telegram_id,
            FoodEntry.eaten_at >= week_start_dt,
        )
    )
    week_entries = week_entries_result.scalars().all()

    total_protein_week = round(sum(e.protein for e in week_entries), 1)
    total_fat_week = round(sum(e.fat for e in week_entries), 1)
    total_carbs_week = round(sum(e.carbs for e in week_entries), 1)

    # Count distinct days in week that have entries
    week_days_with_entries = len(
        set(e.eaten_at.date().isoformat() for e in week_entries)
    )
    div = max(1, week_days_with_entries)

    return StatsOverviewSchema(
        total_entries=total_entries,
        total_calories_consumed=total_calories_consumed,
        avg_calories_per_day=avg_calories_per_day,
        streak_days=streak_days,
        best_day=best_day,
        today_calories=today_calories,
        today_goal=today_goal,
        today_percent=today_percent,
        weekly_calories=weekly_calories,
        monthly_calories=monthly_calories,
        macro_totals_week=MacroAvgSchema(
            protein=total_protein_week,
            fat=total_fat_week,
            carbs=total_carbs_week,
        ),
        macro_avg_week=MacroAvgSchema(
            protein=round(total_protein_week / div, 1),
            fat=round(total_fat_week / div, 1),
            carbs=round(total_carbs_week / div, 1),
        ),
    )
