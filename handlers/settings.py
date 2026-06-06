import logging

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database import set_lang
from locales import t

logger = logging.getLogger(__name__)
router = Router()


def _lang_keyboard(current_lang: str):
    b = InlineKeyboardBuilder()
    b.button(text=("✅ " if current_lang == "en" else "") + "🇬🇧 English", callback_data="lang:en")
    b.button(text=("✅ " if current_lang == "ru" else "") + "🇷🇺 Русский", callback_data="lang:ru")
    b.button(text=("✅ " if current_lang == "uz" else "") + "🇺🇿 O'zbek", callback_data="lang:uz")
    b.button(text=t("back", current_lang), callback_data="menu:back")
    b.adjust(2, 1, 1)
    return b.as_markup()


@router.callback_query(F.data == "menu:settings")
async def cb_settings(callback: CallbackQuery, db_user: dict) -> None:
    lang = db_user["lang"]
    texts = {
        "ru": "⚙️ <b>Настройки</b>\n\nВыбери язык:",
        "uz": "⚙️ <b>Sozlamalar</b>\n\nTilni tanlang:",
        "en": "⚙️ <b>Settings</b>\n\nChoose your language:",
    }
    await callback.message.edit_text(texts.get(lang, texts["en"]), reply_markup=_lang_keyboard(lang))
    await callback.answer()


@router.callback_query(F.data.startswith("lang:"))
async def cb_set_lang(callback: CallbackQuery, db_user: dict) -> None:
    new_lang = callback.data.split(":", 1)[1]
    if new_lang not in ("en", "ru", "uz"):
        await callback.answer()
        return

    await set_lang(callback.from_user.id, new_lang)
    await callback.message.edit_reply_markup(reply_markup=_lang_keyboard(new_lang))

    ack = {"en": "✅ Language set!", "ru": "✅ Язык установлен!", "uz": "✅ Til o'rnatildi!"}
    await callback.answer(ack.get(new_lang, "✅"), show_alert=False)
