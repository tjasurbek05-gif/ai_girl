import logging
from typing import Callable, Awaitable, Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from database import get_user, create_user

logger = logging.getLogger(__name__)

SUPPORTED_LANGS = {"en", "ru", "uz"}


class RegisterMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict], Awaitable[Any]],
        event: TelegramObject,
        data: dict,
    ) -> Any:
        db_user = None
        is_new_user = False

        # aiogram 3 injects the real user here automatically
        tg_user = data.get("event_from_user")

        if tg_user and not tg_user.is_bot:
            db_user = await get_user(tg_user.id)
            if db_user is None:
                raw_lang = (tg_user.language_code or "en")[:2].lower()
                lang = raw_lang if raw_lang in SUPPORTED_LANGS else "en"
                try:
                    db_user = await create_user(tg_user.id, lang)
                    is_new_user = True
                    logger.info("Registered new user %s (lang=%s)", tg_user.id, lang)
                except Exception as exc:
                    logger.exception("Failed to register user %s: %s", tg_user.id, exc)

        data["db_user"] = db_user
        data["is_new_user"] = is_new_user
        return await handler(event, data)
