from aiogram import Router

from .start import router as start_router
from .onboarding import router as onboarding_router
from .admin import router as admin_router


def get_main_router() -> Router:
    router = Router()
    router.include_router(start_router)
    router.include_router(onboarding_router)
    router.include_router(admin_router)
    return router
