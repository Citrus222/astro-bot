# database.py

import sqlite3
from datetime import datetime

DB_NAME = “astro_bot.db”

def init_db():
conn = sqlite3.connect(DB_NAME)
c = conn.cursor()
c.execute(’’’
CREATE TABLE IF NOT EXISTS users (
user_id     INTEGER PRIMARY KEY,
username    TEXT,
full_name   TEXT,
requests    INTEGER DEFAULT 0,
is_premium  INTEGER DEFAULT 0,
joined_at   TEXT
)
‘’’)
conn.commit()
conn.close()

def get_user(user_id: int):
conn = sqlite3.connect(DB_NAME)
c = conn.cursor()
c.execute(“SELECT * FROM users WHERE user_id = ?”, (user_id,))
row = c.fetchone()
conn.close()
return row

def add_user(user_id: int, username: str, full_name: str):
conn = sqlite3.connect(DB_NAME)
c = conn.cursor()
c.execute(’’’
INSERT OR IGNORE INTO users (user_id, username, full_name, joined_at)
VALUES (?, ?, ?, ?)
‘’’, (user_id, username, full_name, datetime.now().isoformat()))
conn.commit()
conn.close()

def increment_requests(user_id: int):
conn = sqlite3.connect(DB_NAME)
c = conn.cursor()
c.execute(“UPDATE users SET requests = requests + 1 WHERE user_id = ?”, (user_id,))
conn.commit()
conn.close()

def get_requests_count(user_id: int) -> int:
user = get_user(user_id)
return user[3] if user else 0

def is_premium(user_id: int) -> bool:
user = get_user(user_id)
return bool(user[4]) if user else False

def set_premium(user_id: int):
conn = sqlite3.connect(DB_NAME)
c = conn.cursor()
c.execute(“UPDATE users SET is_premium = 1 WHERE user_id = ?”, (user_id,))
conn.commit()
conn.close()
