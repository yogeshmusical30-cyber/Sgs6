import sqlite3
from pathlib import Path
DB_PATH = Path(__file__).with_name('sgs.db')

def init_db():
    with sqlite3.connect(DB_PATH) as db:
        db.execute('CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY, message TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP)')
