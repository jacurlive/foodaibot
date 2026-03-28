import base64
import json
import logging
from dataclasses import dataclass
from typing import Optional

from openai import AsyncOpenAI, OpenAIError

from bot.config import settings

logger = logging.getLogger(__name__)


@dataclass
class FoodAnalysisResult:
    dish_name: str
    calories: float
    protein: float
    fat: float
    carbs: float
    description: str
    grams: int = 100
    is_food: bool = True


LANGUAGE_INSTRUCTIONS = {
    "ru": "Write dish_name and description in Russian.",
    "en": "Write dish_name and description in English.",
    "uz": "Write dish_name and description in Uzbek.",
}

BASE_ANALYSIS_PROMPT = """You are a professional nutritionist and food analyst.
Analyze the food in the image and provide nutritional information.

Respond ONLY with a valid JSON object in this exact format:
{{
  "is_food": true,
  "dish_name": "Name of the dish",
  "grams": 250,
  "calories": 350,
  "protein": 25.5,
  "fat": 12.0,
  "carbs": 40.0,
  "description": "Brief description of the dish and its main ingredients (1-2 sentences)"
}}

Rules:
- {lang_instruction}
- If there is no food in the image, set "is_food": false and use 0 for all numeric fields
- All numeric values must be numbers (not strings)
- Calories are in kcal, macros are in grams
- grams is the estimated weight of the portion shown in the photo
- Estimate values specifically for the portion size visible in the photo
- Be precise and realistic with nutritional values
- Keep description concise and informative"""


def get_analysis_prompt(lang: str) -> str:
    lang_instruction = LANGUAGE_INSTRUCTIONS.get(lang, LANGUAGE_INSTRUCTIONS["en"])
    return BASE_ANALYSIS_PROMPT.format(lang_instruction=lang_instruction)


STUB_MODE = False

STUB_RESULT = FoodAnalysisResult(
    is_food=True,
    dish_name="Куриная грудка с рисом",
    calories=420,
    protein=38.5,
    fat=8.2,
    carbs=48.0,
    description="Отварная куриная грудка с варёным белым рисом. Богато белком, умеренно по калориям.",
)


class OpenAIService:
    def __init__(self):
        self.model = settings.OPENAI_MODEL
        if not STUB_MODE:
            self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def analyze_food_photo(
        self, photo_bytes: bytes, lang: str = "en"
    ) -> Optional[FoodAnalysisResult]:
        if STUB_MODE:
            logger.info("STUB MODE: returning fake food analysis result")
            return STUB_RESULT

        try:
            image_b64 = base64.b64encode(photo_bytes).decode("utf-8")
            prompt = get_analysis_prompt(lang)

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt,
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_b64}",
                                    "detail": "high",
                                },
                            },
                        ],
                    }
                ],
                max_tokens=500,
                temperature=0.1,
            )

            content = response.choices[0].message.content.strip()

            if content.startswith("```"):
                lines = content.split("\n")
                content = "\n".join(lines[1:-1])

            data = json.loads(content)

            return FoodAnalysisResult(
                is_food=data.get("is_food", True),
                dish_name=data.get("dish_name", "Unknown dish"),
                grams=int(data.get("grams", 100)),
                calories=float(data.get("calories", 0)),
                protein=float(data.get("protein", 0)),
                fat=float(data.get("fat", 0)),
                carbs=float(data.get("carbs", 0)),
                description=data.get("description", ""),
            )

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse OpenAI response as JSON: {e}")
            return None
        except OpenAIError as e:
            logger.error(f"OpenAI API error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in food analysis: {e}")
            raise
