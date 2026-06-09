import json
import logging
import os

from aiogram import Router, F
from aiogram.types import Message

logger = logging.getLogger(__name__)
router = Router()

import os
ADMIN_IDS = {int(os.getenv('SUPER_ADMIN_ID', 0))}
JSON_PATH = "/root/ai_girl/characters/characters.json"


def load_chars():
    with open(JSON_PATH, encoding="utf-8") as f:
        return json.load(f)


def save_chars(data):
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


@router.message(F.photo & F.from_user.id.in_(ADMIN_IDS))
async def handle_admin_photo(message: Message) -> None:
    caption = (message.caption or "").strip().lower()
    file_id = message.photo[-1].file_id

    if not caption:
        await message.answer(
            "📸 Send photo with caption:\n"
            "<code>malika</code> — sets avatar\n"
            "<code>malika tashkent_cafe</code> — sets scenario photo"
        )
        return

    parts = caption.split()
    char_id = parts[0]
    scene_id = parts[1] if len(parts) > 1 else None

    chars = load_chars()
    char = next((c for c in chars if c["id"] == char_id), None)

    if not char:
        await message.answer(f"❌ Character <code>{char_id}</code> not found.\nAvailable: {', '.join(c['id'] for c in chars)}")
        return

    if scene_id:
        scene = next((s for s in char.get("scenarios", []) if s["id"] == scene_id), None)
        if not scene:
            available = ", ".join(s["id"] for s in char.get("scenarios", []))
            await message.answer(f"❌ Scenario <code>{scene_id}</code> not found.\nAvailable: {available}")
            return
        scene["photo_file_id"] = file_id
        save_chars(chars)
        await message.answer(f"✅ <b>{char['name']}</b> → <code>{scene_id}</code> photo set!")
    else:
        char["photo_file_id"] = file_id
        save_chars(chars)
        await message.answer(f"✅ <b>{char['name']}</b> avatar set!")
