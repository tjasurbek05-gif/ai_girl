from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import WebAppInfo

from ai.prompts import CHARACTERS, Character
from config import config
from locales import t


# ── Language select ───────────────────────────────────────────────────────────

def lang_keyboard() -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(text="🇬🇧 English", callback_data="lang:en")
    b.button(text="🇷🇺 Русский", callback_data="lang:ru")
    b.button(text="🇺🇿 O'zbek", callback_data="lang:uz")
    b.adjust(2)
    return b.as_markup()


# ── Main menu ─────────────────────────────────────────────────────────────────

def main_menu_keyboard(lang: str):
    b = InlineKeyboardBuilder()
    # Characters button opens Mini App directly
    if lang == "ru":
        b.button(text="💬 Персонажи", web_app=WebAppInfo(url="https://velvet-app.duckdns.org/"))
        b.button(text="👤 Профиль",   callback_data="menu:profile")
        b.button(text="🛍️ Магазин",  callback_data="menu:shop")
        b.button(text="💎 Гемы",      callback_data="menu:gems_store")
        b.button(text="⚙️ Настройки", callback_data="menu:settings")
    elif lang == "uz":
        b.button(text="💬 Qahramonlar", web_app=WebAppInfo(url="https://velvet-app.duckdns.org/"))
        b.button(text="👤 Profil",      callback_data="menu:profile")
        b.button(text="🛍️ Do'kon",    callback_data="menu:shop")
        b.button(text="💎 Gemlar",     callback_data="menu:gems_store")
        b.button(text="⚙️ Sozlamalar", callback_data="menu:settings")
    else:
        b.button(text="💬 Characters", web_app=WebAppInfo(url="https://velvet-app.duckdns.org/"))
        b.button(text="👤 Profile",    callback_data="menu:profile")
        b.button(text="🛍️ Shop",      callback_data="menu:shop")
        b.button(text="💎 Gems Store", callback_data="menu:gems_store")
        b.button(text="⚙️ Settings",   callback_data="menu:settings")
    b.adjust(2, 2, 1)
    return b.as_markup()



# ── Character list ────────────────────────────────────────────────────────────

def characters_keyboard(lang: str) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    for char in CHARACTERS:
        b.button(text=f"{char.avatar} {char.name}", callback_data=f"char:{char.id}")
    b.button(text=t("back", lang), callback_data="menu:back")
    b.adjust(1)
    return b.as_markup()


# ── Scenario list ─────────────────────────────────────────────────────────────

def scenarios_keyboard(character: Character, lang: str) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    for scenario in character.scenarios:
        title = scenario.title.get(lang, scenario.title["en"])
        if scenario.gems_cost > 0:
            title = f"{title}  💎{scenario.gems_cost}"
        b.button(text=title, callback_data=f"scene:{character.id}:{scenario.id}")
    b.button(text=t("back", lang), callback_data="menu:characters")
    b.adjust(1)
    return b.as_markup()


# ── In-chat controls ──────────────────────────────────────────────────────────

def chat_keyboard(lang: str) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(text=t("reset_chat", lang),    callback_data="chat:reset")
    b.button(text=t("animate_btn", lang),   callback_data="chat:animate")
    b.button(text=t("main_menu_btn", lang), callback_data="chat:menu")
    b.adjust(2, 1)
    return b.as_markup()


def no_energy_keyboard(lang: str) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    if lang == "ru":
        b.button(text="🛍️ Магазин", callback_data="menu:shop")
        b.button(text="🏠 Меню",    callback_data="menu:back")
    else:
        b.button(text="🛍️ Shop",       callback_data="menu:shop")
        b.button(text="🏠 Main Menu",   callback_data="menu:back")
    b.adjust(2)
    return b.as_markup()


# ── Shop ──────────────────────────────────────────────────────────────────────

_PLANS = [
    ("2days",   config.PRICE_2DAYS,   config.GEMS_2DAYS,   {"en": "2 Days",   "ru": "2 Дня"}),
    ("1month",  config.PRICE_1MONTH,  config.GEMS_1MONTH,  {"en": "1 Month",  "ru": "1 Месяц"}),
    ("3months", config.PRICE_3MONTHS, config.GEMS_3MONTHS, {"en": "3 Months", "ru": "3 Месяца"}),
    ("1year",   config.PRICE_1YEAR,   config.GEMS_1YEAR,   {"en": "1 Year",   "ru": "1 Год"}),
]


def shop_keyboard(lang: str) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    for plan_key, stars, gems, labels in _PLANS:
        label = labels.get(lang, labels["en"])
        b.button(
            text=f"⭐ {stars} — {label}  (+💎{gems})",
            callback_data=f"buy:{plan_key}",
        )
    b.button(text=t("back", lang), callback_data="menu:back")
    b.adjust(1)
    return b.as_markup()


def get_plan_meta(plan_key: str) -> dict | None:
    """Return metadata for a plan key, or None if unknown."""
    for key, stars, gems, labels in _PLANS:
        if key == plan_key:
            return {"key": key, "stars": stars, "gems": gems, "labels": labels}
    return None


# ── Gems Store ────────────────────────────────────────────────────────────────

_GEMS_PACKS = [
    ("gems_85",   149,  85,   None),
    ("gems_210",  349,  210,  "best"),
    ("gems_540",  899,  540,  None),
    ("gems_1360", 2249, 1360, None),
    ("gems_2720", 2499, 2720, "value"),
    ("gems_5000", 4999, 5000, None),
]


def gems_store_keyboard(lang: str) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    for pack_id, stars, gems, badge in _GEMS_PACKS:
        prefix = "🔥 " if badge else ""
        b.button(text=f"{prefix}💎 {gems} — ⭐{stars}", callback_data=f"buygems:{pack_id}")
    b.button(text=t("back", lang), callback_data="menu:back")
    b.adjust(1)
    return b.as_markup()


def get_gems_pack_meta(pack_id: str) -> dict | None:
    """Return metadata for a gems pack id, or None if unknown."""
    for key, stars, gems, badge in _GEMS_PACKS:
        if key == pack_id:
            return {"key": key, "stars": stars, "gems": gems, "badge": badge}
    return None


# ── Generic back ──────────────────────────────────────────────────────────────

def back_to_menu_keyboard(lang: str) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(text=t("main_menu_btn", lang), callback_data="menu:back")
    return b.as_markup()
