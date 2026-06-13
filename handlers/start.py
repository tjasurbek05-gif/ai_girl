import json
import logging
from datetime import datetime

from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message, CallbackQuery, WebAppInfo,
    InlineKeyboardMarkup, InlineKeyboardButton,
    KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove,
)

from database import get_user, get_energy, is_premium, set_referrer
from keyboards import lang_keyboard, main_menu_keyboard
from locales import t
from states import ChatStates

logger = logging.getLogger(__name__)
router = Router()

WEBAPP_URL = "https://velvet-app.duckdns.org"


def main_menu_kb(lang: str) -> ReplyKeyboardMarkup:
    """Reply keyboard with WebApp button — this is what makes sendData() work."""
    choose_label = {
        "ru": "💬 Выбрать персонажа",
        "uz": "💬 Qahramonni tanlash",
        "en": "💬 Choose Character",
    }.get(lang, "💬 Choose Character")

    shop_label = {
        "ru": "🛍️ Магазин",
        "uz": "🛍️ Do'kon",
        "en": "🛍️ Shop",
    }.get(lang, "🛍️ Shop")

    profile_label = {
        "ru": "👤 Профиль",
        "uz": "👤 Profil",
        "en": "👤 Profile",
    }.get(lang, "👤 Profile")

    settings_label = {
        "ru": "⚙️ Настройки",
        "uz": "⚙️ Sozlamalar",
        "en": "⚙️ Settings",
    }.get(lang, "⚙️ Settings")

    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(
                text=choose_label,
                web_app=WebAppInfo(url=WEBAPP_URL)
            )],
            [KeyboardButton(text=shop_label), KeyboardButton(text=profile_label)],
            [KeyboardButton(text=settings_label)],
        ],
        resize_keyboard=True,
    )


async def send_main_menu(target: Message | CallbackQuery, lang: str) -> None:
    user_id = target.from_user.id
    user = await get_user(user_id)
    energy = await get_energy(user_id)
    premium = await is_premium(user_id)
    gems = user["gems"] if user else 0

    if premium and user and user.get("sub_expires"):
        try:
            exp = datetime.fromisoformat(user["sub_expires"])
            sub_line = t("sub_active", lang, expires=exp.strftime("%d %b %Y"))
        except ValueError:
            sub_line = t("sub_none", lang)
    else:
        sub_line = t("sub_none", lang)

    text = t("main_menu", lang, energy=energy, gems=gems, sub_line=sub_line)
    kb = main_menu_kb(lang)

    if isinstance(target, CallbackQuery):
        await target.message.answer(text, reply_markup=kb)
        await target.answer()
    else:
        await target.answer(text, reply_markup=kb)


@router.message(CommandStart(deep_link=True))
async def cmd_start(
    message: Message,
    db_user: dict | None,
    state: FSMContext,
    command: CommandObject,
    is_new_user: bool = False,
) -> None:
    await state.clear()

    if is_new_user and command.args and command.args.startswith("ref_"):
        try:
            referrer_id = int(command.args[len("ref_"):])
            await set_referrer(message.from_user.id, referrer_id)
        except ValueError:
            pass

    if db_user is None:
        await message.answer(t("choose_lang", "en"), reply_markup=lang_keyboard())
        return
    await send_main_menu(message, db_user["lang"])


@router.message(Command("menu"))
async def cmd_menu(message: Message, db_user: dict | None, state: FSMContext) -> None:
    await state.clear()
    lang = db_user["lang"] if db_user else "en"
    await send_main_menu(message, lang)


# ── Handle WebApp data (sent via sendData()) ──────────────────────────────────
@router.message(F.web_app_data)
async def handle_webapp_data(message: Message, db_user: dict, state: FSMContext) -> None:
    lang = db_user["lang"] if db_user else "en"
    try:
        data = json.loads(message.web_app_data.data)

        action = data.get("action")
        if action == "custom_character_request":
            await message.answer(t("custom_character_soon", lang))
            return
        if action == "buy_gems":
            pack_id = data.get("pack_id")
            from handlers.shop import send_gems_invoice
            ok = await send_gems_invoice(message.bot, message.from_user.id, pack_id, lang)
            if not ok:
                await message.answer(t("error_generic", lang))
            return

        char_id  = data.get("char_id")
        scene_id = data.get("scene_id")

        if not char_id or not scene_id:
            await message.answer(t("error_generic", lang))
            return

        # Set FSM state and redirect to chat handler
        await state.set_state(ChatStates.chatting)
        await state.update_data(char_id=char_id, scene_id=scene_id)

        # Import here to avoid circular import
        from ai.prompts import get_character, get_scenario
        char     = get_character(char_id)
        scenario = get_scenario(char_id, scene_id)

        if not char or not scenario:
            await message.answer(t("error_generic", lang))
            return

        opening = scenario.opening.get(lang, scenario.opening["en"])

        from database import get_history, save_history
        history = await get_history(message.from_user.id, char_id, scene_id)
        is_new  = len(history) == 0

        from handlers.chat import chat_keyboard
        kb = chat_keyboard(lang)

        if is_new:
            if scenario.photo_file_id:
                await message.answer_photo(
                    photo=scenario.photo_file_id,
                    caption=f"{char.avatar} <b>{char.name}</b>\n\n{opening}",
                    reply_markup=kb,
                )
            else:
                await message.answer(
                    f"{char.avatar} <b>{char.name}</b>\n\n{opening}",
                    reply_markup=kb,
                )
            await save_history(message.from_user.id, char_id, scene_id,
                               [{"role": "assistant", "content": opening}])
        else:
            await message.answer(t("chat_continue", lang), reply_markup=kb)

    except (json.JSONDecodeError, KeyError) as e:
        logger.error("WebApp data parse error: %s", e)
        await message.answer(t("error_generic", lang))


@router.callback_query(F.data == "menu:back")
async def cb_menu_back(callback: CallbackQuery, db_user: dict, state: FSMContext) -> None:
    await state.clear()
    await send_main_menu(callback, db_user["lang"])
