from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class UserSchema(BaseModel):
    id: int
    telegram_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    goal: Optional[str] = None
    units: str
    daily_calories: Optional[float] = None
    language: str
    is_onboarded: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserUpdateSchema(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    goal: Optional[str] = None
    units: Optional[str] = None
    language: Optional[str] = None


class CompleteOnboardingSchema(BaseModel):
    name: str
    age: int
    gender: str
    height: float
    weight: float
    goal: str
    units: str
    language: Optional[str] = None


class FoodEntrySchema(BaseModel):
    id: int
    user_id: int
    dish_name: str
    calories: float
    protein: float
    fat: float
    carbs: float
    description: Optional[str] = None
    photo_file_id: Optional[str] = None
    eaten_at: datetime

    class Config:
        from_attributes = True


class MacroTotals(BaseModel):
    calories: float
    protein: float
    fat: float
    carbs: float


class DiaryDaySchema(BaseModel):
    date: str
    entries: List[FoodEntrySchema]
    totals: MacroTotals


class DiaryTodaySchema(BaseModel):
    date: str
    entries: List[FoodEntrySchema]
    totals: MacroTotals
    remaining_calories: float


class DiaryWeekSchema(BaseModel):
    days: List[DiaryDaySchema]


class DiaryHistorySchema(BaseModel):
    entries: List[FoodEntrySchema]
    total: int
    page: int
    pages: int


class DeleteResponseSchema(BaseModel):
    ok: bool


class CalorieDaySchema(BaseModel):
    date: str
    calories: float


class MacroAvgSchema(BaseModel):
    protein: float
    fat: float
    carbs: float


class StatsOverviewSchema(BaseModel):
    total_entries: int
    total_calories_consumed: float
    avg_calories_per_day: float
    streak_days: int
    best_day: Optional[str] = None
    today_calories: float
    today_goal: float
    today_percent: float
    weekly_calories: List[CalorieDaySchema]
    monthly_calories: List[CalorieDaySchema]
    macro_totals_week: MacroAvgSchema
    macro_avg_week: MacroAvgSchema


class FoodAnalyzeResponseSchema(BaseModel):
    dish_name: str
    grams: int
    calories: float
    protein: float
    fat: float
    carbs: float
    description: str
    is_food: bool


class FoodSaveSchema(BaseModel):
    dish_name: str
    grams: Optional[int] = None
    calories: float
    protein: float
    fat: float
    carbs: float
    description: Optional[str] = None
    photo_file_id: Optional[str] = None
