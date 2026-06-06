import logging
from datetime import datetime

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database import get_user, get_energy, is_premium
from keyboards import lang_keyboard, main_menu_keyboard, characters_keyboard
from locales import t

logger = logging.getLogger(__name__)
router = Router()


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
    kb = main_menu_keyboard(lang)

    if isinstance(target, CallbackQuery):
        await target.message.edit_text(text, reply_markup=kb)
        await target.answer()
    else:
        await target.answer(text, reply_markup=kb)


@router.message(CommandStart())
async def cmd_start(message: Message, db_user: dict | None, state: FSMContext) -> None:
    await state.clear()
    if db_user is None:
        await message.answer(t("choose_lang", "en"), reply_markup=lang_keyboard())
        return
    await send_main_menu(message, db_user["lang"])


@router.message(Command("menu"))
async def cmd_menu(message: Message, db_user: dict | None, state: FSMContext) -> None:
    await state.clear()
    lang = db_user["lang"] if db_user else "en"
    await send_main_menu(message, lang)


@router.callback_query(F.data == "menu:back")
async def cb_menu_back(callback: CallbackQuery, db_user: dict | None, state: FSMContext) -> None:
    await state.clear()
    if db_user is None:
        await callback.answer("Please send /start first.", show_alert=True)
        return
    await send_main_menu(callback, db_user["lang"])


@router.callback_query(F.data == "menu:characters")
async def cb_menu_characters(callback: CallbackQuery, db_user: dict | None) -> None:
    if db_user is None:
        await callback.answer("Please send /start first.", show_alert=True)
        return
    lang = db_user["lang"]
    await callback.message.edit_text(
        t("choose_character", lang),
        reply_markup=characters_keyboard(lang),
    )
    await callback.answer()
