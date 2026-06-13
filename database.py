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
        await db.execute("""
            CREATE TABLE IF NOT EXISTS admins (
                user_id    INTEGER PRIMARY KEY,
                added_by   INTEGER,
                added_at   TEXT DEFAULT (datetime('now'))
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS message_log (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                date    TEXT    DEFAULT (DATE('now'))
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS processed_messages (
                user_id    INTEGER NOT NULL,
                message_id INTEGER NOT NULL,
                created_at TEXT DEFAULT (datetime('now')),
                PRIMARY KEY (user_id, message_id)
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS user_items (
                user_id INTEGER,
                item_id TEXT,
                PRIMARY KEY (user_id, item_id)
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS referrals (
                user_id     INTEGER PRIMARY KEY,
                referrer_id INTEGER NOT NULL,
                rewarded    INTEGER DEFAULT 0,
                created_at  TEXT DEFAULT (datetime('now'))
            )
        """)

        # Additive column migrations (safe to re-run on an existing DB)
        for col_def in (
            "last_animate_date TEXT DEFAULT ''",
            "last_broadcast_date TEXT DEFAULT ''",
        ):
            try:
                await db.execute(f"ALTER TABLE users ADD COLUMN {col_def}")
            except Exception:
                pass  # column already exists

        await db.commit()
 
 
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
 
 
async def log_purchase(user_id: int, stars: int, plan: str, gems_delta: int):
    async with aiosqlite.connect(DB) as db:
        await db.execute(
            "INSERT INTO purchases (user_id, stars, plan, gems_delta) VALUES (?,?,?,?)",
            (user_id, stars, plan, gems_delta)
        )
        await db.commit()
 
 
async def is_admin(user_id: int) -> bool:
    from config import config
    if user_id == config.SUPER_ADMIN_ID:
        return True
    async with aiosqlite.connect(DB) as db:
        async with db.execute(
            "SELECT 1 FROM admins WHERE user_id=?", (user_id,)
        ) as cur:
            return await cur.fetchone() is not None
 
 
async def add_admin(user_id: int, added_by: int) -> None:
    async with aiosqlite.connect(DB) as db:
        await db.execute(
            "INSERT OR IGNORE INTO admins (user_id, added_by) VALUES (?,?)",
            (user_id, added_by)
        )
        await db.commit()
 
 
async def remove_admin(user_id: int) -> None:
    async with aiosqlite.connect(DB) as db:
        await db.execute("DELETE FROM admins WHERE user_id=?", (user_id,))
        await db.commit()
 
 
async def get_admins() -> list[dict]:
    async with aiosqlite.connect(DB) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM admins ORDER BY added_at") as cur:
            return [dict(r) for r in await cur.fetchall()]
 
 
async def log_message(user_id: int) -> None:
    async with aiosqlite.connect(DB) as db:
        await db.execute(
            "INSERT INTO message_log (user_id) VALUES (?)", (user_id,)
        )
        await db.commit()
 
 
async def get_stats() -> dict:
    async with aiosqlite.connect(DB) as db:
        async with db.execute("SELECT COUNT(*) FROM users") as cur:
            total_users = (await cur.fetchone())[0]
        async with db.execute(
            "SELECT COUNT(*) FROM users WHERE DATE(created_at)=DATE('now')"
        ) as cur:
            new_today = (await cur.fetchone())[0]
        async with db.execute(
            "SELECT COUNT(*) FROM users "
            "WHERE sub_expires != '' AND sub_expires > datetime('now')"
        ) as cur:
            premium_users = (await cur.fetchone())[0]
        async with db.execute(
            "SELECT COUNT(DISTINCT user_id) FROM message_log WHERE date=DATE('now')"
        ) as cur:
            active_today = (await cur.fetchone())[0]
        async with db.execute(
            "SELECT COUNT(*) FROM message_log WHERE date=DATE('now')"
        ) as cur:
            messages_today = (await cur.fetchone())[0]
        async with db.execute(
            "SELECT COUNT(*), COALESCE(SUM(stars),0) FROM purchases "
            "WHERE DATE(created_at)=DATE('now')"
        ) as cur:
            row = await cur.fetchone()
            purchases_today, revenue_today = row[0], row[1]
        async with db.execute(
            "SELECT COALESCE(SUM(stars),0) FROM purchases"
        ) as cur:
            revenue_total = (await cur.fetchone())[0]
 
    return {
        "total_users":     total_users,
        "new_today":       new_today,
        "premium_users":   premium_users,
        "active_today":    active_today,
        "messages_today":  messages_today,
        "purchases_today": purchases_today,
        "revenue_today":   revenue_today,
        "revenue_total":   revenue_total,
    }
 
 
async def is_message_processed(user_id: int, message_id: int) -> bool:
    async with aiosqlite.connect(DB) as db:
        async with db.execute(
            "SELECT 1 FROM processed_messages WHERE user_id=? AND message_id=?",
            (user_id, message_id)
        ) as cur:
            return await cur.fetchone() is not None
 
 
async def mark_message_processed(user_id: int, message_id: int) -> None:
    async with aiosqlite.connect(DB) as db:
        await db.execute(
            "INSERT OR IGNORE INTO processed_messages (user_id, message_id) VALUES (?,?)",
            (user_id, message_id)
        )
        await db.commit()
 
 
async def cleanup_old_processed(days: int = 3) -> None:
    async with aiosqlite.connect(DB) as db:
        await db.execute(
            "DELETE FROM processed_messages WHERE created_at < datetime('now', ?)",
            (f"-{days} days",)
        )
        await db.commit()


# ── Affiliate / referrals ───────────────────────────────────────────────────

async def set_referrer(user_id: int, referrer_id: int) -> bool:
    """Record referrer for a brand-new user. Returns False if already set or self-referral."""
    if user_id == referrer_id:
        return False
    async with aiosqlite.connect(DB) as db:
        cur = await db.execute(
            "INSERT OR IGNORE INTO referrals (user_id, referrer_id) VALUES (?,?)",
            (user_id, referrer_id)
        )
        await db.commit()
        return cur.rowcount > 0


async def get_referral_stats(user_id: int) -> dict:
    async with aiosqlite.connect(DB) as db:
        async with db.execute(
            "SELECT COUNT(*) FROM referrals WHERE referrer_id=?", (user_id,)
        ) as cur:
            count = (await cur.fetchone())[0]
        async with db.execute(
            "SELECT COALESCE(SUM(gems_delta),0) FROM purchases WHERE plan='referral_bonus' AND user_id=?",
            (user_id,)
        ) as cur:
            earned = (await cur.fetchone())[0]
    return {"referrals": count, "gems_earned": earned}


async def maybe_award_referral_bonus(user_id: int, bonus_gems: int = 20) -> int | None:
    """If this user was referred and hasn't triggered a reward yet, credit the referrer.
    Returns referrer_id if a bonus was awarded, else None."""
    async with aiosqlite.connect(DB) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT referrer_id, rewarded FROM referrals WHERE user_id=?", (user_id,)
        ) as cur:
            row = await cur.fetchone()
        if not row or row["rewarded"]:
            return None
        referrer_id = row["referrer_id"]
        await db.execute("UPDATE referrals SET rewarded=1 WHERE user_id=?", (user_id,))
        await db.execute("UPDATE users SET gems=gems+? WHERE user_id=?", (bonus_gems, referrer_id))
        await db.execute(
            "INSERT INTO purchases (user_id, stars, plan, gems_delta) VALUES (?,0,'referral_bonus',?)",
            (referrer_id, bonus_gems)
        )
        await db.commit()
    return referrer_id


# ── Animate / re-engagement helpers ─────────────────────────────────────────

async def get_last_animate_date(user_id: int) -> str:
    user = await get_user(user_id)
    return (user.get("last_animate_date") or "") if user else ""


async def set_last_animate_date(user_id: int, date_str: str) -> None:
    async with aiosqlite.connect(DB) as db:
        await db.execute("UPDATE users SET last_animate_date=? WHERE user_id=?", (date_str, user_id))
        await db.commit()


async def mark_broadcast_sent(user_id: int, date_str: str) -> None:
    async with aiosqlite.connect(DB) as db:
        await db.execute("UPDATE users SET last_broadcast_date=? WHERE user_id=?", (date_str, user_id))
        await db.commit()


async def get_inactive_chats(days: int = 1) -> list[dict]:
    """Latest chat per user that hasn't been touched in >= `days` days
    and hasn't already received today's re-engagement broadcast."""
    async with aiosqlite.connect(DB) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("""
            SELECT c.user_id, c.character_id, c.scenario_id, c.updated_at, u.lang
            FROM chats c
            JOIN users u ON u.user_id = c.user_id
            WHERE c.updated_at = (
                SELECT MAX(c2.updated_at) FROM chats c2 WHERE c2.user_id = c.user_id
            )
            AND c.updated_at <= datetime('now', ?)
            AND COALESCE(u.last_broadcast_date, '') != DATE('now')
        """, (f"-{days} days",)) as cur:
            rows = await cur.fetchall()
    return [dict(r) for r in rows]
