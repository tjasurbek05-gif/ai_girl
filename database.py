import aiosqlite
import json
from datetime import datetime, date
from config import config


DB = config.DB_PATH


async def init_db():
    async with aiosqlite.connect(DB) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id     INTEGER PRIMARY KEY,
                lang        TEXT DEFAULT 'en',
                energy      INTEGER DEFAULT 49,
                energy_date TEXT DEFAULT '',
                gems        INTEGER DEFAULT 0,
                sub_expires TEXT DEFAULT '',
                created_at  TEXT DEFAULT (datetime('now'))
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS chats (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id      INTEGER,
                character_id TEXT,
                scenario_id  TEXT,
                history      TEXT DEFAULT '[]',
                updated_at   TEXT DEFAULT (datetime('now')),
                UNIQUE(user_id, character_id, scenario_id)
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS purchases (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id    INTEGER,
                stars      INTEGER,
                plan       TEXT,
                gems_delta INTEGER,
                created_at TEXT DEFAULT (datetime('now'))
            )
        """)
        await db.commit()


# ── Users ─────────────────────────────────────────────────────────────────────

async def get_user(user_id: int) -> dict | None:
    async with aiosqlite.connect(DB) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM users WHERE user_id=?", (user_id,)) as cur:
            row = await cur.fetchone()
            return dict(row) if row else None


async def create_user(user_id: int, lang: str = "en") -> dict:
    async with aiosqlite.connect(DB) as db:
        await db.execute(
            "INSERT OR IGNORE INTO users (user_id, lang) VALUES (?, ?)",
            (user_id, lang)
        )
        await db.commit()
    return await get_user(user_id)


async def set_lang(user_id: int, lang: str):
    async with aiosqlite.connect(DB) as db:
        await db.execute("UPDATE users SET lang=? WHERE user_id=?", (lang, user_id))
        await db.commit()


async def get_energy(user_id: int) -> int:
    """Returns current energy, resets to 49 if new day."""
    async with aiosqlite.connect(DB) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT energy, energy_date FROM users WHERE user_id=?", (user_id,)
        ) as cur:
            row = await cur.fetchone()
        today = str(date.today())
        if row["energy_date"] != today:
            await db.execute(
                "UPDATE users SET energy=49, energy_date=? WHERE user_id=?",
                (today, user_id)
            )
            await db.commit()
            return 49
        return row["energy"]


async def consume_energy(user_id: int) -> bool:
    """Returns True if energy was consumed, False if 0."""
    energy = await get_energy(user_id)
    if energy <= 0:
        return False
    async with aiosqlite.connect(DB) as db:
        await db.execute(
            "UPDATE users SET energy=energy-1 WHERE user_id=?", (user_id,)
        )
        await db.commit()
    return True


async def add_gems(user_id: int, amount: int):
    async with aiosqlite.connect(DB) as db:
        await db.execute(
            "UPDATE users SET gems=gems+? WHERE user_id=?", (amount, user_id)
        )
        await db.commit()


async def spend_gems(user_id: int, amount: int) -> bool:
    user = await get_user(user_id)
    if not user or user["gems"] < amount:
        return False
    async with aiosqlite.connect(DB) as db:
        await db.execute(
            "UPDATE users SET gems=gems-? WHERE user_id=?", (amount, user_id)
        )
        await db.commit()
    return True


async def set_subscription(user_id: int, expires: str, gems: int):
    async with aiosqlite.connect(DB) as db:
        await db.execute(
            "UPDATE users SET sub_expires=?, gems=gems+? WHERE user_id=?",
            (expires, gems, user_id)
        )
        await db.commit()


async def is_premium(user_id: int) -> bool:
    user = await get_user(user_id)
    if not user or not user["sub_expires"]:
        return False
    try:
        exp = datetime.fromisoformat(user["sub_expires"])
        return exp > datetime.now()
    except Exception:
        return False


# ── Chat history ──────────────────────────────────────────────────────────────

async def get_history(user_id: int, character_id: str, scenario_id: str) -> list:
    async with aiosqlite.connect(DB) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT history FROM chats WHERE user_id=? AND character_id=? AND scenario_id=?",
            (user_id, character_id, scenario_id)
        ) as cur:
            row = await cur.fetchone()
            return json.loads(row["history"]) if row else []


async def save_history(user_id: int, character_id: str, scenario_id: str, history: list):
    async with aiosqlite.connect(DB) as db:
        await db.execute("""
            INSERT INTO chats (user_id, character_id, scenario_id, history, updated_at)
            VALUES (?, ?, ?, ?, datetime('now'))
            ON CONFLICT(user_id, character_id, scenario_id)
            DO UPDATE SET history=excluded.history, updated_at=excluded.updated_at
        """, (user_id, character_id, scenario_id, json.dumps(history)))
        await db.commit()


async def clear_history(user_id: int, character_id: str, scenario_id: str):
    async with aiosqlite.connect(DB) as db:
        await db.execute(
            "DELETE FROM chats WHERE user_id=? AND character_id=? AND scenario_id=?",
            (user_id, character_id, scenario_id)
        )
        await db.commit()


# ── Purchases ─────────────────────────────────────────────────────────────────

async def log_purchase(user_id: int, stars: int, plan: str, gems_delta: int):
    async with aiosqlite.connect(DB) as db:
        await db.execute(
            "INSERT INTO purchases (user_id, stars, plan, gems_delta) VALUES (?,?,?,?)",
            (user_id, stars, plan, gems_delta)
        )
        await db.commit()
