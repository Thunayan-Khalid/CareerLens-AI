import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "recruitai.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                score INTEGER NOT NULL,
                level TEXT NOT NULL,
                matched_count INTEGER NOT NULL,
                missing_count INTEGER NOT NULL,
                created_at TEXT NOT NULL
            )
        """)

def save_analysis(filename, result):
    with get_connection() as conn:
        cur = conn.execute("""
            INSERT INTO analyses
            (filename, score, level, matched_count, missing_count, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            filename, result["score"], result["level"],
            len(result["matched_skills"]), len(result["missing_skills"]),
            datetime.now().strftime("%Y-%m-%d %H:%M")
        ))
        return cur.lastrowid

def get_history():
    with get_connection() as conn:
        return conn.execute("SELECT * FROM analyses ORDER BY id DESC LIMIT 50").fetchall()
