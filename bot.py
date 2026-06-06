import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import config
from database import init_db
from middlewares import RegisterMiddleware
from handlers import start, chat, shop, settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s — %(message)s",
)
logger = logging.getLogger(__name__)


async def main() -> None:
    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=MemoryStorage())

    dp.update.middleware(RegisterMiddleware())

    # Order matters: specific handlers first, catch-all last
    dp.include_router(chat.router)
    dp.include_router(shop.router)
    dp.include_router(settings.router)
    dp.include_router(start.router)

    await init_db()
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("Bot started.")

    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
