"""Create a consistent SQLite backup using SQLite's online backup API.

Usage:
    python scripts/backup_db.py
    python scripts/backup_db.py --output D:\backups\belajar-lagi.db
"""
import argparse
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from database.database import DB_PATH  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description="Backup database Belajar Lagi.")
    parser.add_argument("--output", help="Path file backup. Default: backups/learning-<waktu>.db")
    args = parser.parse_args()

    source_path = Path(DB_PATH)
    if not source_path.exists():
        raise SystemExit(f"Database tidak ditemukan: {source_path}")

    if args.output:
        target_path = Path(args.output).expanduser().resolve()
    else:
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        target_path = ROOT / "backups" / f"learning-{stamp}.db"
    target_path.parent.mkdir(parents=True, exist_ok=True)

    source = sqlite3.connect(source_path)
    target = sqlite3.connect(target_path)
    try:
        source.backup(target)
    finally:
        target.close()
        source.close()

    print(f"Backup dibuat: {target_path}")


if __name__ == "__main__":
    main()
