"""
FastAPI backend for the Velvet Mini App.
Runs alongside the bot on the same VPS, reads the same SQLite DB.
Start with: uvicorn api:app --host 0.0.0.0 --port 8000
"""
import hmac
import hashlib
import json
import urllib.parse
from typing import Any

from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware

from config import config
from database import get_user, get_energy, is_premium
import aiosqlite

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Telegram initData verification ───────────────────────────────────────────

def verify_init_data(init_data: str) -> dict:
    """Verify Telegram WebApp initData and return parsed user dict."""
    parsed = dict(urllib.parse.parse_qsl(init_data, keep_blank_values=True))
    received_hash = parsed.pop("hash", "")

    data_check = "\n".join(f"{k}={v}" for k, v in sorted(parsed.items()))
    secret = hmac.new(b"WebAppData", config.BOT_TOKEN.encode(), hashlib.sha256).digest()
    expected = hmac.new(secret, data_check.encode(), hashlib.sha256).hexdigest()

    if not hmac.compare_digest(expected, received_hash):
        raise HTTPException(status_code=401, detail="Invalid initData")

    user_json = parsed.get("user", "{}")
    return json.loads(user_json)


async def get_uid(x_init_data: str = Header(...)) -> int:
    """Dependency: verify initData and return user_id."""
    tg_user = verify_init_data(x_init_data)
    return int(tg_user["id"])


# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/api/user")
async def api_user(x_init_data: str = Header(...)):
    user_id = await get_uid(x_init_data)
    user = await get_user(user_id)
    if not user:
        raise HTTPException(404, "User not found")
    energy  = await get_energy(user_id)
    premium = await is_premium(user_id)
    return {
        "user_id":     user_id,
        "lang":        user["lang"],
        "energy":      energy,
        "gems":        user["gems"],
        "premium":     premium,
        "sub_expires": user.get("sub_expires", ""),
        "bot_username": config.BOT_USERNAME,
    }


@app.get("/api/chats")
async def api_chats(x_init_data: str = Header(...)):
    user_id = await get_uid(x_init_data)
    async with aiosqlite.connect(config.DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            """SELECT character_id, scenario_id, history, updated_at
               FROM chats
               WHERE user_id = ?
               ORDER BY updated_at DESC""",
            (user_id,)
        ) as cur:
            rows = await cur.fetchall()

    result = []
    for row in rows:
        history = json.loads(row["history"] or "[]")
        last_msg = ""
        for msg in reversed(history):
            if msg.get("role") == "assistant":
                last_msg = msg.get("content", "")[:80]
                break
        if history:
            result.append({
                "character_id": row["character_id"],
                "scenario_id":  row["scenario_id"],
                "last_message": last_msg,
                "updated_at":   row["updated_at"],
            })
    return result


@app.get("/api/shop/items")
async def api_shop_items():
    """Return shop items (static for now)."""
    return [
        {"id": "animal_ears",   "name": {"en": "Animal Ears",   "ru": "Ушки",          "uz": "Hayvon quloqlari"}, "price": 190, "emoji": "🐱"},
        {"id": "body_hair_gel", "name": {"en": "Body Hair Gel", "ru": "Гель для тела",  "uz": "Tanaga gel"},       "price": 155, "emoji": "✨"},
        {"id": "bondage_rope",  "name": {"en": "Bondage Rope",  "ru": "Верёвка",        "uz": "Arqon"},            "price": 70,  "emoji": "🪢"},
        {"id": "butt_plug",     "name": {"en": "Butt Plug",     "ru": "Пробка",         "uz": "Probka"},           "price": 45,  "emoji": "💎"},
        {"id": "collar",        "name": {"en": "Collar",        "ru": "Ошейник",        "uz": "Yoqa"},             "price": 80,  "emoji": "🔗"},
        {"id": "blindfold",     "name": {"en": "Blindfold",     "ru": "Повязка",        "uz": "Ko'z bog'i"},       "price": 60,  "emoji": "🎭"},
        {"id": "handcuffs",     "name": {"en": "Handcuffs",     "ru": "Наручники",      "uz": "Qo'l kishanlar"},   "price": 95,  "emoji": "⛓️"},
        {"id": "feather",       "name": {"en": "Feather",       "ru": "Перо",           "uz": "Pat"},              "price": 40,  "emoji": "🪶"},
        {"id": "control_orb",   "name": {"en": "Control Orb",   "ru": "Сфера контроля", "uz": "Boshqaruv shari"},  "price": 300, "emoji": "🔮"},
        {"id": "wine_bottle",   "name": {"en": "Bottle of Wine","ru": "Бутылка вина",   "uz": "Vino shishasi"},    "price": 12,  "emoji": "🍷"},
        {"id": "cute_pajamas",  "name": {"en": "Cute Pajamas",  "ru": "Милая пижама",   "uz": "Yoqimli pijama"},   "price": 50,  "emoji": "🩱"},
        {"id": "rose_bouquet",  "name": {"en": "Rose Bouquet",  "ru": "Букет роз",      "uz": "Atirgul guldastasi"}, "price": 25, "emoji": "💐"},
        {"id": "perfume",       "name": {"en": "Perfume",       "ru": "Духи",           "uz": "Parfyum"},          "price": 65,  "emoji": "🧴"},
        {"id": "jewelry_box",   "name": {"en": "Jewelry Box",   "ru": "Шкатулка",       "uz": "Taqinchoq qutisi"}, "price": 180, "emoji": "💍"},
    ]


@app.post("/api/shop/buy/{item_id}")
async def api_buy_item(item_id: str, x_init_data: str = Header(...)):
    user_id = await get_uid(x_init_data)
    items = await api_shop_items()
    item = next((i for i in items if i["id"] == item_id), None)
    if not item:
        raise HTTPException(404, "Item not found")

    user = await get_user(user_id)
    if not user or user["gems"] < item["price"]:
        raise HTTPException(400, "Not enough gems")

    from database import spend_gems
    ok = await spend_gems(user_id, item["price"])
    if not ok:
        raise HTTPException(400, "Not enough gems")

    # Store purchased item
    async with aiosqlite.connect(config.DB_PATH) as db:
        await db.execute(
            "CREATE TABLE IF NOT EXISTS user_items (user_id INTEGER, item_id TEXT, PRIMARY KEY(user_id, item_id))"
        )
        await db.execute(
            "INSERT OR IGNORE INTO user_items (user_id, item_id) VALUES (?,?)",
            (user_id, item_id)
        )
        await db.commit()

    return {"ok": True, "gems_left": user["gems"] - item["price"]}


@app.get("/api/shop/owned")
async def api_owned_items(x_init_data: str = Header(...)):
    user_id = await get_uid(x_init_data)
    async with aiosqlite.connect(config.DB_PATH) as db:
        await db.execute(
            "CREATE TABLE IF NOT EXISTS user_items (user_id INTEGER, item_id TEXT, PRIMARY KEY(user_id, item_id))"
        )
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT item_id FROM user_items WHERE user_id=?", (user_id,)
        ) as cur:
            rows = await cur.fetchall()
    return [r["item_id"] for r in rows]


@app.post("/api/user/lang/{lang_code}")
async def api_set_lang(lang_code: str, x_init_data: str = Header(...)):
    if lang_code not in ("en", "ru", "uz"):
        raise HTTPException(400, "Invalid language")
    user_id = await get_uid(x_init_data)
    from database import set_lang
    await set_lang(user_id, lang_code)
    return {"ok": True}


@app.get("/api/gems/packs")
async def api_gems_packs():
    """Return purchasable gem packs (static for now). Purchases happen via the bot's Stars invoice."""
    return [
        {"id": "gems_85",   "gems": 85,   "stars": 149,  "badge": None},
        {"id": "gems_210",  "gems": 210,  "stars": 349,  "badge": "best"},
        {"id": "gems_540",  "gems": 540,  "stars": 899,  "badge": None},
        {"id": "gems_1360", "gems": 1360, "stars": 2249, "badge": None},
        {"id": "gems_2720", "gems": 2720, "stars": 2499, "badge": "value"},
        {"id": "gems_5000", "gems": 5000, "stars": 4999, "badge": None},
    ]


@app.get("/api/referral/stats")
async def api_referral_stats(x_init_data: str = Header(...)):
    user_id = await get_uid(x_init_data)
    from database import get_referral_stats
    return await get_referral_stats(user_id)
