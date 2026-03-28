from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
import os

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


# Serve React SPA — must be AFTER all API routes
DIST_DIR = os.path.join(os.path.dirname(__file__), "..", "webapp", "dist")

if os.path.isdir(DIST_DIR):
    app.mount("/assets", StaticFiles(directory=os.path.join(DIST_DIR, "assets")), name="assets")

    @app.get("/{full_path:path}")
    async def spa(full_path: str):
        return FileResponse(os.path.join(DIST_DIR, "index.html"))
