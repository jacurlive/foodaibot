import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from bot.config import settings
from bot.database import session_pool
from bot.handlers import get_main_router
from bot.middlewares import DbSessionMiddleware, UserMiddleware


def setup_logging():
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    log_dir = os.path.dirname(settings.LOG_FILE)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)

    handlers = [logging.StreamHandler(sys.stdout)]
    try:
        handlers.append(logging.FileHandler(settings.LOG_FILE, encoding="utf-8"))
    except Exception:
        pass

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=handlers,
    )
    # Suppress noisy loggers
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("aiogram").setLevel(logging.INFO)


async def main():
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting FoodAI bot...")

    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Register middlewares on specific event types (order matters)
    for observer in (dp.message, dp.callback_query):
        observer.middleware(DbSessionMiddleware(session_pool))
        observer.middleware(UserMiddleware())

    # Include all routers
    dp.include_router(get_main_router())

    # Log bot info
    bot_info = await bot.get_me()
    logger.info(f"Bot started: @{bot_info.username} (id={bot_info.id})")

    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        logger.info("Bot stopped.")
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
