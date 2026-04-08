import aiosqlite
from datetime import datetime

DB_PATH = "data/mila_bot.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY,
                title TEXT,
                date TEXT,
                relevance TEXT,
                captured_at TEXT
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS profiles (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE,
                platform TEXT,
                last_collected TEXT
            )
        """)
        await db.commit()

# Idempotência: só insere se não existir na última hora
async def save_event(title: str, date: str, relevance: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO events (title, date, relevance, captured_at) VALUES (?, ?, ?, ?)",
            (title, date, relevance, datetime.now().isoformat())
        )
        await db.commit()