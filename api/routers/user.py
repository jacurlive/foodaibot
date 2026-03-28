from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import get_session, get_current_user
from api.schemas import UserSchema, UserUpdateSchema, CompleteOnboardingSchema
from bot.models.user import User
from bot.services.user_service import UserService

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/me", response_model=UserSchema)
async def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user


@router.put("/me", response_model=UserSchema)
async def update_me(
    data: UserUpdateSchema,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    if data.name is not None:
        current_user.name = data.name
    if data.age is not None:
        current_user.age = data.age
    if data.gender is not None:
        current_user.gender = data.gender
    if data.height is not None:
        current_user.height = data.height
    if data.weight is not None:
        current_user.weight = data.weight
    if data.goal is not None:
        current_user.goal = data.goal
    if data.units is not None:
        current_user.units = data.units
    if data.language is not None:
        current_user.language = data.language

    # Recalculate daily calories if profile is complete
    new_calories = current_user.calculate_daily_calories()
    if new_calories is not None:
        current_user.daily_calories = new_calories

    await session.commit()
    await session.refresh(current_user)
    return current_user


@router.post("/complete-onboarding", response_model=UserSchema)
async def complete_onboarding(
    data: CompleteOnboardingSchema,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    current_user.name = data.name
    current_user.age = data.age
    current_user.gender = data.gender
    current_user.height = data.height
    current_user.weight = data.weight
    current_user.goal = data.goal
    current_user.units = data.units
    if data.language:
        current_user.language = data.language
    current_user.is_onboarded = True
    calories = current_user.calculate_daily_calories()
    if calories:
        current_user.daily_calories = calories
    await session.commit()
    await session.refresh(current_user)
    return current_user
