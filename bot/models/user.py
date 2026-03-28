from sqlalchemy import BigInteger, String, Integer, Float, Boolean, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from datetime import datetime
import enum

from .base import Base


class Language(str, enum.Enum):
    RU = "ru"
    EN = "en"
    UZ = "uz"


class Gender(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"


class Goal(str, enum.Enum):
    LOSE = "lose"
    MAINTAIN = "maintain"
    GAIN = "gain"


class Units(str, enum.Enum):
    METRIC = "metric"
    IMPERIAL = "imperial"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    username: Mapped[str | None] = mapped_column(String(64), nullable=True)
    first_name: Mapped[str | None] = mapped_column(String(128), nullable=True)

    # Onboarding
    language: Mapped[str] = mapped_column(String(5), default="en", nullable=False)
    is_onboarded: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Profile
    name: Mapped[str | None] = mapped_column(String(128), nullable=True)
    age: Mapped[int | None] = mapped_column(Integer, nullable=True)
    gender: Mapped[str | None] = mapped_column(String(10), nullable=True)
    height: Mapped[float | None] = mapped_column(Float, nullable=True)  # cm
    weight: Mapped[float | None] = mapped_column(Float, nullable=True)  # kg
    goal: Mapped[str | None] = mapped_column(String(10), nullable=True)
    units: Mapped[str] = mapped_column(String(10), default="metric", nullable=False)

    # Daily calorie norm (calculated)
    daily_calories: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Notifications
    notify_morning: Mapped[bool] = mapped_column(Boolean, default=False)
    notify_afternoon: Mapped[bool] = mapped_column(Boolean, default=False)
    notify_evening: Mapped[bool] = mapped_column(Boolean, default=False)

    # Admin
    is_banned: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    def calculate_daily_calories(self) -> float | None:
        """Mifflin-St Jeor formula."""
        if not all([self.age, self.gender, self.height, self.weight, self.goal]):
            return None

        if self.gender == "male":
            bmr = 10 * self.weight + 6.25 * self.height - 5 * self.age + 5
        else:
            bmr = 10 * self.weight + 6.25 * self.height - 5 * self.age - 161

        # Activity factor: moderate (1.55)
        tdee = bmr * 1.55

        if self.goal == "lose":
            return round(tdee - 500)
        elif self.goal == "gain":
            return round(tdee + 300)
        else:
            return round(tdee)

    def get_weight_display(self) -> str:
        if self.units == "imperial" and self.weight:
            return f"{round(self.weight * 2.20462, 1)} lb"
        return f"{self.weight} kg" if self.weight else "—"

    def get_height_display(self) -> str:
        if self.units == "imperial" and self.height:
            inches = self.height / 2.54
            feet = int(inches // 12)
            inch = round(inches % 12, 1)
            return f"{feet}'{inch}\""
        return f"{self.height} cm" if self.height else "—"
