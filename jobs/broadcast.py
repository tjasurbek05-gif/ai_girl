import asyncio
import logging
from datetime import datetime

from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest

from ai.prompts import get_character, get_scenario
from database import get_inactive_chats, mark_broadcast_sent
from locales import t

logger = logging.getLogger(__name__)

_BROADCAST_INTERVAL = 60 * 60 * 6  # check every 6 hours


async def run_daily_broadcast(bot: Bot, days_inactive: int = 1) -> None:
    """Send a personalized re-engagement message to users inactive for `days_inactive`+ days."""
    today = datetime.now().strftime("%Y-%m-%d")
    chats = await get_inactive_chats(days=days_inactive)

    for chat in chats:
        user_id  = chat["user_id"]
        lang     = chat["lang"] or "en"
        char_id  = chat["character_id"]
        scene_id = chat["scenario_id"]

        char     = get_character(char_id)
        scenario = get_scenario(char_id, scene_id)
        if not char or not scenario:
            continue

        name     = char.name
        scenario_title = scenario.title.get(lang, scenario.title["en"])

        try:
            await bot.send_message(
                user_id,
                t("reengagement_msg", lang, name=name, scenario=scenario_title),
            )
        except (TelegramForbiddenError, TelegramBadRequest):
            pass
        except Exception:
            logger.exception("Failed to send re-engagement message to %s", user_id)

        await mark_broadcast_sent(user_id, today)


async def broadcast_scheduler(bot: Bot) -> None:
    """Background loop — periodically runs the re-engagement broadcast."""
    while True:
        try:
            await run_daily_broadcast(bot)
        except Exception:
            logger.exception("Broadcast run failed")
        await asyncio.sleep(_BROADCAST_INTERVAL)
