-- Velvet bot database schema
-- Apply with: sqlite3 velvet.db < db/schema.sql
-- Or via database.py init_db() which runs these statements directly.

CREATE TABLE IF NOT EXISTS users (
    user_id     INTEGER PRIMARY KEY,
    lang        TEXT    DEFAULT 'en',
    energy      INTEGER DEFAULT 49,
    energy_date TEXT    DEFAULT '',
    gems        INTEGER DEFAULT 0,
    sub_expires TEXT    DEFAULT '',
    created_at  TEXT    DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS chats (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id      INTEGER NOT NULL,
    character_id TEXT    NOT NULL,
    scenario_id  TEXT    NOT NULL,
    history      TEXT    DEFAULT '[]',
    updated_at   TEXT    DEFAULT (datetime('now')),
    UNIQUE(user_id, character_id, scenario_id)
);

CREATE TABLE IF NOT EXISTS purchases (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER NOT NULL,
    stars      INTEGER NOT NULL,
    plan       TEXT    NOT NULL,
    gems_delta INTEGER NOT NULL,
    created_at TEXT    DEFAULT (datetime('now'))
);

-- Indexes for common query patterns
CREATE INDEX IF NOT EXISTS idx_chats_user    ON chats(user_id);
CREATE INDEX IF NOT EXISTS idx_purchases_user ON purchases(user_id);
