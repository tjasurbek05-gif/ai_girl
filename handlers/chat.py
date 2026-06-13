import logging
import json
from collections import defaultdict
from datetime import datetime, timedelta
 
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
 
from ai import get_ai_reply, build_system_prompt
from ai.prompts import get_character, get_scenario
from database import (
    get_user, get_energy, consume_energy, is_premium,
    spend_gems, get_history, save_history, clear_history,
    log_message, is_message_processed, mark_message_processed,
    get_last_animate_date, set_last_animate_date,
)
from keyboards import scenarios_keyboard, chat_keyboard, no_energy_keyboard
from locales import t
from states import ChatStates
 
logger = logging.getLogger(__name__)
router = Router()
 
# ── Rate limiting (in-memory) ─────────────────────────────────────────────────
_rate: dict[int, list[datetime]] = defaultdict(list)
_RATE_LIMIT  = 10
_RATE_WINDOW = timedelta(seconds=60)
_MAX_MSG_LEN = 1000

# ── Animate ───────────────────────────────────────────────────────────────────
_ANIMATE_GEMS_COST = 50
 
 
def _is_rate_limited(user_id: int) -> bool:
    now = datetime.now()
    _rate[user_id] = [ts for ts in _rate[user_id] if now - ts < _RATE_WINDOW]
    if len(_rate[user_id]) >= _RATE_LIMIT:
        return True
    _rate[user_id].append(now)
    return False
 
 
@router.message(F.web_app_data)
async def handle_webapp_data(message: Message, db_user: dict, state: FSMContext) -> None:
    lang = db_user["lang"]
    try:
        data = json.loads(message.web_app_data.data)
    except Exception:
        return
 
    char_id  = data.get("char_id")
    scene_id = data.get("scene_id")
    resume   = data.get("resume", False)
 
    if not char_id or not scene_id:
        return
 
    char     = get_character(char_id)
    scenario = get_scenario(char_id, scene_id)
    user_id  = message.from_user.id
 
    if not char or not scenario:
        await message.answer(t("error_generic", lang))
        return
 
    await state.set_state(ChatStates.chatting)
    await state.update_data(char_id=char_id, scene_id=scene_id)
 
    history = await get_history(user_id, char_id, scene_id)
    opening = scenario.opening.get(lang, scenario.opening["en"])
 
    if not history or not resume:
        history = [{"role": "assistant", "content": opening}]
        await save_history(user_id, char_id, scene_id, history)
        text = f"{char.avatar} <b>{char.name}</b>\n\n{opening}"
    else:
        last = next((m["content"] for m in reversed(history) if m["role"] == "assistant"), opening)
        text = f"{char.avatar} <b>{char.name}</b>\n\n<i>Continuing...</i>\n\n{last}"
 
    if scenario.photo_file_id:
        await message.answer_photo(
            photo=scenario.photo_file_id,
            caption=text,
            reply_markup=chat_keyboard(lang),
        )
    else:
        await message.answer(text, reply_markup=chat_keyboard(lang))
 
 
@router.callback_query(F.data.startswith("char:"))
async def cb_character(callback: CallbackQuery, db_user: dict) -> None:
    char_id = callback.data.split(":", 1)[1]
    char = get_character(char_id)
    lang = db_user["lang"]
 
    if not char:
        await callback.answer(t("error_generic", lang), show_alert=True)
        return
 
    text = t(
        "character_card", lang,
        avatar=char.avatar,
        name=char.name,
        tagline=char.tagline.get(lang, char.tagline["en"]),
    )
 
    if char.photo_file_id:
        await callback.message.delete()
        await callback.bot.send_photo(
            chat_id=callback.from_user.id,
            photo=char.photo_file_id,
            caption=text,
            reply_markup=scenarios_keyboard(char, lang),
        )
    else:
        await callback.message.edit_text(text, reply_markup=scenarios_keyboard(char, lang))
 
    await callback.answer()
 
 
@router.callback_query(F.data.startswith("scene:"))
async def cb_scenario(callback: CallbackQuery, db_user: dict, state: FSMContext) -> None:
    _, char_id, scene_id = callback.data.split(":", 2)
    lang = db_user["lang"]
    user_id = callback.from_user.id
 
    char = get_character(char_id)
    scenario = get_scenario(char_id, scene_id)
 
    if not char or not scenario:
        await callback.answer(t("error_generic", lang), show_alert=True)
        return
 
    if scenario.gems_cost > 0:
        history = await get_history(user_id, char_id, scene_id)
        if not history:
            user = await get_user(user_id)
            gems = user["gems"] if user else 0
            if gems < scenario.gems_cost:
                await callback.answer(
                    t("not_enough_gems", lang, cost=scenario.gems_cost, gems=gems),
                    show_alert=True,
                )
                return
            await spend_gems(user_id, scenario.gems_cost)
            await callback.answer(t("gems_spent", lang, cost=scenario.gems_cost), show_alert=True)
 
    await state.set_state(ChatStates.chatting)
    await state.update_data(char_id=char_id, scene_id=scene_id)
 
    history = await get_history(user_id, char_id, scene_id)
    is_new  = len(history) == 0
    opening = scenario.opening.get(lang, scenario.opening["en"])
 
    await callback.message.delete()
 
    if is_new:
        if scenario.photo_file_id:
            await callback.bot.send_photo(
                chat_id=user_id,
                photo=scenario.photo_file_id,
                caption=f"{char.avatar} <b>{char.name}</b>\n\n{opening}",
                reply_markup=chat_keyboard(lang),
            )
        else:
            await callback.bot.send_message(
                chat_id=user_id,
                text=f"{char.avatar} <b>{char.name}</b>\n\n{opening}",
                reply_markup=chat_keyboard(lang),
            )
        history = [{"role": "assistant", "content": opening}]
        await save_history(user_id, char_id, scene_id, history)
        await log_message(user_id)
    else:
        await callback.bot.send_message(
            chat_id=user_id,
            text=t("chat_continue", lang),
            reply_markup=chat_keyboard(lang),
        )
 
    await callback.answer()
 
 
@router.message(ChatStates.chatting, F.text)
async def handle_chat_message(message: Message, db_user: dict, state: FSMContext) -> None:
    lang    = db_user["lang"]
    user_id = message.from_user.id
 
    # 1. Deduplication
    if await is_message_processed(user_id, message.message_id):
        logger.warning("Duplicate message_id=%d user=%d — skipped", message.message_id, user_id)
        return
 
    # 2. Length guard
    if len(message.text) > _MAX_MSG_LEN:
        await message.answer(f"⚠️ Message too long (max {_MAX_MSG_LEN} chars).")
        return
 
    # 3. Rate limit
    if _is_rate_limited(user_id):
        logger.warning("Rate limit hit — user=%d", user_id)
        await message.answer("⏳ Slow down! Max 10 messages per minute.")
        return
 
    # 4. FSM sanity
    fsm_data = await state.get_data()
    char_id  = fsm_data.get("char_id")
    scene_id = fsm_data.get("scene_id")
 
    if not char_id or not scene_id:
        await state.clear()
        await message.answer(t("error_generic", lang))
        return
 
    char     = get_character(char_id)
    scenario = get_scenario(char_id, scene_id)
 
    if not char or not scenario:
        await state.clear()
        await message.answer(t("error_generic", lang))
        return
 
    # 5. Energy
    premium = await is_premium(user_id)
    if not premium:
        if not await consume_energy(user_id):
            await message.answer(t("no_energy", lang), reply_markup=no_energy_keyboard(lang))
            return
 
    # 6. Call AI
    scene_title   = scenario.title.get(lang, scenario.title["en"])
    scene_desc    = scenario.description.get(lang, scenario.description["en"])
    system_prompt = build_system_prompt(char.personality, scene_title, scene_desc, lang)
    history       = await get_history(user_id, char_id, scene_id)
 
    await message.bot.send_chat_action(chat_id=user_id, action="typing")
    reply = await get_ai_reply(system_prompt, history, message.text)
 
    if reply is None:
        await message.answer(t("ai_error", lang))
        return
 
    # 7. Save & respond
    history.append({"role": "user",      "content": message.text})
    history.append({"role": "assistant", "content": reply})
    await save_history(user_id, char_id, scene_id, history)
    await log_message(user_id)
    await mark_message_processed(user_id, message.message_id)
 
    await message.answer(f"{char.avatar} {reply}", reply_markup=chat_keyboard(lang))
 
 
@router.callback_query(F.data == "chat:reset")
async def cb_chat_reset(callback: CallbackQuery, db_user: dict, state: FSMContext) -> None:
    lang    = db_user["lang"]
    user_id = callback.from_user.id
 
    fsm_data = await state.get_data()
    char_id  = fsm_data.get("char_id")
    scene_id = fsm_data.get("scene_id")
 
    if char_id and scene_id:
        await clear_history(user_id, char_id, scene_id)
 
    char     = get_character(char_id) if char_id else None
    scenario = get_scenario(char_id, scene_id) if char_id and scene_id else None
 
    if char and scenario:
        opening = scenario.opening.get(lang, scenario.opening["en"])
        history = [{"role": "assistant", "content": opening}]
        await save_history(user_id, char_id, scene_id, history)
        await callback.message.edit_text(
            f"{char.avatar} <b>{char.name}</b>\n\n{opening}",
            reply_markup=chat_keyboard(lang),
        )
 
    await callback.answer(t("chat_reset_done", lang))
 
 
@router.callback_query(F.data == "chat:animate")
async def cb_chat_animate(callback: CallbackQuery, db_user: dict, state: FSMContext) -> None:
    lang    = db_user["lang"]
    user_id = callback.from_user.id

    fsm_data = await state.get_data()
    char_id  = fsm_data.get("char_id")
    scene_id = fsm_data.get("scene_id")

    scenario = get_scenario(char_id, scene_id) if char_id and scene_id else None
    if not scenario or not scenario.photo_file_id:
        await callback.answer(t("animate_unavailable", lang), show_alert=True)
        return

    premium = await is_premium(user_id)
    today = datetime.now().strftime("%Y-%m-%d")

    if premium and await get_last_animate_date(user_id) != today:
        await set_last_animate_date(user_id, today)
    else:
        user = await get_user(user_id)
        gems = user["gems"] if user else 0
        if gems < _ANIMATE_GEMS_COST:
            await callback.answer(
                t("not_enough_gems", lang, cost=_ANIMATE_GEMS_COST, gems=gems),
                show_alert=True,
            )
            return
        await spend_gems(user_id, _ANIMATE_GEMS_COST)

    await callback.answer(t("animate_soon", lang), show_alert=True)


@router.callback_query(F.data == "chat:menu")
async def cb_chat_menu(callback: CallbackQuery, db_user: dict, state: FSMContext) -> None:
    await state.clear()
    from handlers.start import send_main_menu
    await send_main_menu(callback, db_user["lang"])
 
 
@router.message(ChatStates.chatting, Command("reset"))
async def cmd_reset(message: Message, db_user: dict, state: FSMContext) -> None:
    lang     = db_user["lang"]
    user_id  = message.from_user.id
    fsm_data = await state.get_data()
    char_id  = fsm_data.get("char_id")
    scene_id = fsm_data.get("scene_id")
 
    if char_id and scene_id:
        await clear_history(user_id, char_id, scene_id)
 
    char     = get_character(char_id) if char_id else None
    scenario = get_scenario(char_id, scene_id) if char_id and scene_id else None
 
    if char and scenario:
        opening = scenario.opening.get(lang, scenario.opening["en"])
        await save_history(user_id, char_id, scene_id, [{"role": "assistant", "content": opening}])
        await message.answer(
            f"{char.avatar} <b>{char.name}</b>\n\n{opening}",
            reply_markup=chat_keyboard(lang),
        )
    else:
        await message.answer(t("chat_reset_done", lang))
