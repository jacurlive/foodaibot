from sqlalchemy import BigInteger, String, Float, DateTime, Text, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime

from .base import Base


class FoodEntry(Base):
    __tablename__ = "food_entries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.telegram_id", ondelete="CASCADE"), nullable=False
    )

    # Food analysis
    dish_name: Mapped[str] = mapped_column(String(256), nullable=False)
    calories: Mapped[float] = mapped_column(Float, nullable=False)
    protein: Mapped[float] = mapped_column(Float, nullable=False)
    fat: Mapped[float] = mapped_column(Float, nullable=False)
    carbs: Mapped[float] = mapped_column(Float, nullable=False)

    # Raw AI response
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Photo
    photo_file_id: Mapped[str | None] = mapped_column(String(256), nullable=True)

    # Timestamp
    eaten_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
