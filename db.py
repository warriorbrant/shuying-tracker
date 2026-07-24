import os
import sqlite3
import time
from pathlib import Path

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
    created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);

CREATE TABLE IF NOT EXISTS novel_chapters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    novel_id INTEGER NOT NULL REFERENCES novels(id) ON DELETE CASCADE,
    chapter_no INTEGER NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL DEFAULT '',
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
"""


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    conn.executescript(SCHEMA)
    conn.commit()
    conn.close()
