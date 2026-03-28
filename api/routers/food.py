from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import get_session, get_current_user
from api.schemas import FoodAnalyzeResponseSchema, FoodSaveSchema, FoodEntrySchema
from bot.models.user import User
from bot.services.diary_service import DiaryService
from bot.services.openai_service import OpenAIService

router = APIRouter(prefix="/food", tags=["food"])

openai_service = OpenAIService()


@router.post("/analyze", response_model=FoodAnalyzeResponseSchema)
async def analyze_food(
    file: UploadFile = File(...),
    lang: str = Form("ru"),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    photo_bytes = await file.read()
    if len(photo_bytes) == 0:
        raise HTTPException(status_code=400, detail="Empty file")

    result = await openai_service.analyze_food_photo(photo_bytes, lang=lang)
    if result is None:
        raise HTTPException(status_code=422, detail="Could not analyze image")

    return FoodAnalyzeResponseSchema(
        dish_name=result.dish_name,
        grams=result.grams,
        calories=result.calories,
        protein=result.protein,
        fat=result.fat,
        carbs=result.carbs,
        description=result.description,
        is_food=result.is_food,
    )


@router.post("/save", response_model=FoodEntrySchema)
async def save_food(
    data: FoodSaveSchema,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    service = DiaryService(session)
    entry = await service.add_entry(
        user_id=current_user.telegram_id,
        dish_name=data.dish_name,
        calories=data.calories,
        protein=data.protein,
        fat=data.fat,
        carbs=data.carbs,
        description=data.description,
        photo_file_id=data.photo_file_id,
    )
    return FoodEntrySchema.model_validate(entry)
