import logging
from typing import Callable, Awaitable, Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from database import get_user, create_user

logger = logging.getLogger(__name__)

SUPPORTED_LANGS = {"en", "ru", "uz"}


class RegisterMiddleware(BaseMiddleware):
    """
    Ensures every real user exists in the DB before the handler runs.
    Injects `db_user: dict | None` into handler data.
    """

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict], Awaitable[Any]],
        event: TelegramObject,
        data: dict,
    ) -> Any:
        db_user: dict | None = None

        tg_user = getattr(event, "from_user", None)
        if tg_user and not tg_user.is_bot:
            db_user = await get_user(tg_user.id)
            if db_user is None:
                # Detect preferred language, fall back to English
                raw_lang = (tg_user.language_code or "en")[:2].lower()
                lang = raw_lang if raw_lang in SUPPORTED_LANGS else "en"
                try:
                    db_user = await create_user(tg_user.id, lang)
                    logger.info("Registered new user %s (lang=%s)", tg_user.id, lang)
                except Exception as exc:
                    logger.exception("Failed to register user %s: %s", tg_user.id, exc)
                    db_user = await get_user(tg_user.id)

        data["db_user"] = db_user
        return await handler(event, data)
