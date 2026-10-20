import os
import sqlite3
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

DB_PATH = os.path.abspath(
    os.environ.get("BELAJAR_LAGI_DB") or os.path.join(ROOT, "learning.db")
)
SCHEMA_PATH = os.path.join(ROOT, "database", "schema.sql")


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA busy_timeout = 5000")
    return conn


def init_db():
    from database.migrations import ensure_indexes, migrate_multi_user

    conn = get_conn()
    try:
        conn.execute("PRAGMA journal_mode = WAL")
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            conn.executescript(f.read())
        conn.commit()
        migrate_multi_user(conn)
        ensure_indexes(conn)
    finally:
        conn.close()
