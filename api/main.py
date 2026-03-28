from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from bot.database import engine
from bot.models.base import Base

from api.routers import user, diary, stats, food


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="FoodAI API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router, prefix="/api")
app.include_router(diary.router, prefix="/api")
app.include_router(stats.router, prefix="/api")
app.include_router(food.router, prefix="/api")


@app.get("/health")
async def health():
    return {"status": "ok"}
