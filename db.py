import os
import sqlite3
import time
from pathlib import Path

from werkzeug.security import generate_password_hash

# Pin the process (and thus SQLite's `datetime('now','localtime')`, and every
# `date.today()`/`datetime.now()` call) to the user's timezone, regardless of
# what timezone the host server happens to run in (e.g. Railway defaults to
# UTC/US time, which made "today" lag behind by most of a day).
os.environ["TZ"] = "Asia/Shanghai"
if hasattr(time, "tzset"):
    time.tzset()

DATA_DIR = Path(os.environ.get("DATA_DIR", Path(__file__).parent))
DB_PATH = Path(os.environ.get("TRACKER_DB_PATH", DATA_DIR / "tracker.db"))

SCHEMA = """
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL CHECK(type IN ('book', 'show')),
    title TEXT NOT NULL,
    creator TEXT DEFAULT '',
    cover_url TEXT DEFAULT '',
    total_units INTEGER,
    unit_label TEXT NOT NULL DEFAULT '页',
    status TEXT NOT NULL DEFAULT '想看',
    rating INTEGER,
    review TEXT DEFAULT '',
    douban_url TEXT DEFAULT '',
    created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);

CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER NOT NULL REFERENCES items(id) ON DELETE CASCADE,
    log_date TEXT NOT NULL,
    minutes_spent INTEGER NOT NULL DEFAULT 0,
    progress_at REAL,
    comment TEXT DEFAULT '',
    created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);

CREATE TABLE IF NOT EXISTS moments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL CHECK(type IN ('stock', 'exercise', 'photo', 'thought')),
    log_date TEXT NOT NULL,
    title TEXT DEFAULT '',
    content TEXT DEFAULT '',
    image_path TEXT DEFAULT '',
    minutes_spent INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);

CREATE TABLE IF NOT EXISTS novels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    summary TEXT DEFAULT '',
    status TEXT NOT NULL DEFAULT '连载中',
    cover_image TEXT DEFAULT '',
    is_locked INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);

CREATE TABLE IF NOT EXISTS novel_volumes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    novel_id INTEGER NOT NULL REFERENCES novels(id) ON DELETE CASCADE,
    volume_no INTEGER NOT NULL,
    title TEXT NOT NULL,
    user_id INTEGER REFERENCES users(id),
    created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);

CREATE TABLE IF NOT EXISTS novel_chapters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    novel_id INTEGER NOT NULL REFERENCES novels(id) ON DELETE CASCADE,
    volume_id INTEGER REFERENCES novel_volumes(id) ON DELETE SET NULL,
    chapter_no INTEGER NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL DEFAULT '',
    is_locked INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);

CREATE TABLE IF NOT EXISTS novel_characters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    novel_id INTEGER NOT NULL REFERENCES novels(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT DEFAULT '',
    image_path TEXT DEFAULT '',
    sort_order INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);

CREATE TABLE IF NOT EXISTS novel_videos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    novel_id INTEGER NOT NULL REFERENCES novels(id) ON DELETE CASCADE,
    title TEXT DEFAULT '',
    source_type TEXT NOT NULL CHECK(source_type IN ('upload', 'link')),
    video_path TEXT DEFAULT '',
    video_url TEXT DEFAULT '',
    thumbnail_path TEXT DEFAULT '',
    duration_seconds INTEGER,
    created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);

CREATE TABLE IF NOT EXISTS novel_chapter_characters (
    chapter_id INTEGER NOT NULL REFERENCES novel_chapters(id) ON DELETE CASCADE,
    character_id INTEGER NOT NULL REFERENCES novel_characters(id) ON DELETE CASCADE,
    PRIMARY KEY (chapter_id, character_id)
);

CREATE TABLE IF NOT EXISTS novel_chapter_videos (
    chapter_id INTEGER NOT NULL REFERENCES novel_chapters(id) ON DELETE CASCADE,
    video_id INTEGER NOT NULL REFERENCES novel_videos(id) ON DELETE CASCADE,
    PRIMARY KEY (chapter_id, video_id)
);

CREATE TABLE IF NOT EXISTS novel_references (
    novel_id INTEGER NOT NULL REFERENCES novels(id) ON DELETE CASCADE,
    item_id INTEGER NOT NULL REFERENCES items(id) ON DELETE CASCADE,
    in_share INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (novel_id, item_id)
);

-- Multi-user groundwork (phase 0): tables exist and content tables get a
-- user_id column (added via migration below, since ALTER TABLE is needed for
-- installs that predate this), but no route enforces ownership yet — that's
-- a later phase. Nothing about current behavior changes by these existing.
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    is_admin INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);

CREATE TABLE IF NOT EXISTS app_settings (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    allow_registration INTEGER NOT NULL DEFAULT 0
);

-- One-time links an admin generates from /admin/users to let a specific
-- account holder set their own new password without email delivery.
CREATE TABLE IF NOT EXISTS password_resets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id),
    token TEXT NOT NULL UNIQUE,
    expires_at TEXT NOT NULL,
    used INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);

-- Raw broker transaction rows, imported from CSV (currently: Schwab's export
-- format). Realized daily P&L is computed on the fly from these (FIFO-match
-- each closing trade against its opening trade(s) per symbol) rather than
-- stored, so it's always consistent and re-uploading never needs a recompute
-- step. dedup_key lets the same file be re-uploaded (or a fresh export that
-- overlaps an earlier one) without creating duplicate rows -- there's no
-- transaction id in the source data, so it's a hash of the row's own fields.
CREATE TABLE IF NOT EXISTS trades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id),
    trade_date TEXT NOT NULL,
    action TEXT NOT NULL,
    symbol TEXT NOT NULL,
    description TEXT DEFAULT '',
    quantity REAL,
    price REAL,
    fees REAL,
    amount REAL NOT NULL,
    dedup_key TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
    UNIQUE(user_id, dedup_key)
);
CREATE INDEX IF NOT EXISTS idx_trades_user_date ON trades(user_id, trade_date);

-- ICBC bank statement rows, imported from password-protected PDF exports.
-- Same dedup-on-reupload approach as `trades` (no bank-provided transaction
-- id either): a fingerprint of the row's own fields.
CREATE TABLE IF NOT EXISTS bank_transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id),
    tx_date TEXT NOT NULL,
    tx_time TEXT DEFAULT '',
    category TEXT DEFAULT '',
    amount REAL NOT NULL,
    balance REAL,
    counterparty_name TEXT DEFAULT '',
    counterparty_account TEXT DEFAULT '',
    channel TEXT DEFAULT '',
    dedup_key TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
    UNIQUE(user_id, dedup_key)
);
CREATE INDEX IF NOT EXISTS idx_bank_transactions_user_date ON bank_transactions(user_id, tx_date);

-- User-drawn routes (click points on a Leaflet map -> polyline, or type
-- place names and geocode them via Nominatim), not imported from anywhere
-- -- see the custom_routes feature. `points` is a JSON array of
-- {"lat":, "lng":, "label":} objects (an object per point rather than a
-- bare [lat, lng] pair, deliberately, so the field names catch a swapped
-- lat/lng bug immediately instead of silently plotting a valid-looking but
-- wrong point); "label" is optional -- present when the point came from a
-- typed-and-geocoded place name, absent for a plain map click. `is_locked`
-- follows the exact same convention as
-- novels.is_locked (1 = only the owner can view, 0 = anyone with the link
-- can) but defaults to locked here, opposite of novels -- a route stays
-- private until its owner explicitly shares it.
CREATE TABLE IF NOT EXISTS custom_routes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id),
    title TEXT NOT NULL DEFAULT '',
    country TEXT NOT NULL DEFAULT '',
    points TEXT NOT NULL,
    is_locked INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);
CREATE INDEX IF NOT EXISTS idx_custom_routes_user_id ON custom_routes(user_id);

-- A chapter can embed any of the author's own routes (for a travelogue --
-- see the /novel feature reused for that). Mirrors novel_chapter_videos'
-- shape exactly. The route's own is_locked is still checked separately
-- when a chapter is read -- attaching a still-private route to a public
-- chapter doesn't make the route itself visible to other readers.
CREATE TABLE IF NOT EXISTS novel_chapter_routes (
    chapter_id INTEGER NOT NULL REFERENCES novel_chapters(id) ON DELETE CASCADE,
    route_id INTEGER NOT NULL REFERENCES custom_routes(id) ON DELETE CASCADE,
    PRIMARY KEY (chapter_id, route_id)
);

-- Indexes on the foreign keys / date columns that every list query filters on.
-- Cheap and idempotent; keeps per-novel and per-item lookups from full-scanning
-- as chapters/logs grow (a novel already has dozens of chapters).
CREATE INDEX IF NOT EXISTS idx_logs_item_id ON logs(item_id);
CREATE INDEX IF NOT EXISTS idx_logs_log_date ON logs(log_date);
CREATE INDEX IF NOT EXISTS idx_moments_log_date ON moments(log_date);
CREATE INDEX IF NOT EXISTS idx_novel_chapters_novel_id ON novel_chapters(novel_id);
CREATE INDEX IF NOT EXISTS idx_novel_characters_novel_id ON novel_characters(novel_id);
CREATE INDEX IF NOT EXISTS idx_novel_videos_novel_id ON novel_videos(novel_id);
"""


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def _migrate(conn):
    # items table predates the douban_url column; patch it in for installs that
    # already exist (CREATE TABLE IF NOT EXISTS above is a no-op for them).
    cols = [row["name"] for row in conn.execute("PRAGMA table_info(items)")]
    if "douban_url" not in cols:
        conn.execute("ALTER TABLE items ADD COLUMN douban_url TEXT DEFAULT ''")

    # novel_references used to store its own title/cover/douban_url per row; it now
    # links to an existing items row instead, so the old shape is dropped and
    # recreated (this table shipped and was redesigned within the same session,
    # no real reference data existed yet to preserve).
    ref_cols = [row["name"] for row in conn.execute("PRAGMA table_info(novel_references)")]
    if ref_cols and "item_id" not in ref_cols:
        conn.execute("DROP TABLE novel_references")
        conn.execute(
            "CREATE TABLE novel_references ("
            "novel_id INTEGER NOT NULL REFERENCES novels(id) ON DELETE CASCADE, "
            "item_id INTEGER NOT NULL REFERENCES items(id) ON DELETE CASCADE, "
            "in_share INTEGER NOT NULL DEFAULT 0, "
            "PRIMARY KEY (novel_id, item_id))"
        )
        ref_cols = ["novel_id", "item_id", "in_share"]
    if ref_cols and "in_share" not in ref_cols:
        conn.execute("ALTER TABLE novel_references ADD COLUMN in_share INTEGER NOT NULL DEFAULT 0")

    novel_cols = [row["name"] for row in conn.execute("PRAGMA table_info(novels)")]
    if novel_cols and "is_locked" not in novel_cols:
        conn.execute("ALTER TABLE novels ADD COLUMN is_locked INTEGER NOT NULL DEFAULT 0")

    chapter_cols = [row["name"] for row in conn.execute("PRAGMA table_info(novel_chapters)")]
    if chapter_cols and "is_locked" not in chapter_cols:
        conn.execute("ALTER TABLE novel_chapters ADD COLUMN is_locked INTEGER NOT NULL DEFAULT 0")
    if chapter_cols and "volume_id" not in chapter_cols:
        conn.execute("ALTER TABLE novel_chapters ADD COLUMN volume_id INTEGER REFERENCES novel_volumes(id) ON DELETE SET NULL")

    # Multi-user phase 0: add a nullable user_id to every owned content table,
    # bootstrap a single admin account (reusing APP_PASSWORD so nothing is
    # locked out by this deploy), and attribute all pre-existing rows to it.
    # No route reads/enforces user_id yet — that's a later phase; this step
    # only makes sure every row has a correct owner once that phase lands.
    owned_tables = [
        "items", "logs", "moments", "novels",
        "novel_chapters", "novel_characters", "novel_videos", "novel_volumes",
    ]
    for table in owned_tables:
        cols = [row["name"] for row in conn.execute(f"PRAGMA table_info({table})")]
        if cols and "user_id" not in cols:
            conn.execute(f"ALTER TABLE {table} ADD COLUMN user_id INTEGER REFERENCES users(id)")

    user_count = conn.execute("SELECT COUNT(*) AS n FROM users").fetchone()["n"]
    if user_count == 0:
        bootstrap_password = os.environ.get("APP_PASSWORD") or "admin"
        conn.execute(
            "INSERT INTO users (username, password_hash, is_admin) VALUES (?, ?, 1)",
            ("admin", generate_password_hash(bootstrap_password, method="pbkdf2:sha256")),
        )

    admin_id = conn.execute("SELECT id FROM users WHERE username = 'admin'").fetchone()
    if admin_id is not None:
        for table in owned_tables:
            cols = [row["name"] for row in conn.execute(f"PRAGMA table_info({table})")]
            if "user_id" in cols:
                conn.execute(
                    f"UPDATE {table} SET user_id = ? WHERE user_id IS NULL", (admin_id["id"],)
                )

    conn.execute("INSERT OR IGNORE INTO app_settings (id, allow_registration) VALUES (1, 0)")


def init_db():
    conn = get_db()
    conn.executescript(SCHEMA)
    conn.commit()
    _migrate(conn)
    conn.commit()
    conn.close()
