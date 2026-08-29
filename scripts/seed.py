import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from app.data.challenges_def import CHALLENGES
from database.database import get_conn, init_db

# lessons seeded: content lives in content/daily/*.md
LESSONS = [
    {"slug": "day01", "title": "Day 01 — Variable & Data Types", "phase": "python", "order": 1, "file": "daily/day01.md"},
    {"slug": "day02", "title": "Day 02 — Operators", "phase": "python", "order": 2, "file": "daily/day02.md"},
    {"slug": "day03", "title": "Day 03 — Conditional", "phase": "python", "order": 3, "file": "daily/day03.md"},
    {"slug": "day04", "title": "Day 04 — Loop", "phase": "python", "order": 4, "file": "daily/day04.md"},
    {"slug": "day05", "title": "Day 05 — Function", "phase": "python", "order": 5, "file": "daily/day05.md"},
    {"slug": "day06", "title": "Day 06 — String", "phase": "python", "order": 6, "file": "daily/day06.md"},
    {"slug": "day07", "title": "Day 07 — List", "phase": "python", "order": 7, "file": "daily/day07.md"},
    {"slug": "day08", "title": "Day 08 — Dictionary", "phase": "python", "order": 8, "file": "daily/day08.md"},
    {"slug": "day09", "title": "Day 09 — Set & Tuple", "phase": "python", "order": 9, "file": "daily/day09.md"},
]

PHASES = [
    {"slug": "python", "title": "Python", "order": 1},
    {"slug": "php", "title": "PHP", "order": 2},
    {"slug": "sql", "title": "SQL", "order": 3},
    {"slug": "codeigniter", "title": "CodeIgniter", "order": 4},
    {"slug": "laravel", "title": "Laravel", "order": 5},
    {"slug": "javascript", "title": "JavaScript", "order": 6},
    {"slug": "se", "title": "Software Engineering", "order": 7},
]

PROJECT = {
    "slug": "employee_management",
    "name": "Employee Management System",
    "stages": [
        ("1", "Stage 1: Python CLI"),
        ("2", "Stage 2: Python + Database"),
        ("3", "Stage 3: FastAPI"),
        ("4", "Stage 4: PHP Native"),
        ("5", "Stage 5: CodeIgniter"),
        ("6", "Stage 6: Laravel"),
        ("7", "Stage 7: JavaScript"),
        ("8", "Stage 8: Docker"),
        ("9", "Stage 9: Deployment"),
    ],
}


def seed():
    init_db()
    conn = get_conn()
    try:
        for p in PHASES:
            conn.execute(
                "INSERT OR IGNORE INTO phases(slug,title,order_index) VALUES(?,?,?)",
                (p["slug"], p["title"], p["order"]))
        for ls in LESSONS:
            conn.execute(
                "INSERT OR IGNORE INTO lessons(slug,title,phase_slug,order_index,content_file) "
                "VALUES(?,?,?,?,?)",
                (ls["slug"], ls["title"], ls["phase"], ls["order"], ls["file"]))
        for c in CHALLENGES:
            conn.execute(
                "INSERT OR IGNORE INTO challenges(slug,title,language,difficulty,topic,statement,"
                "starter_code,hint1,hint2,test_json) VALUES(?,?,?,?,?,?,?,?,?,?)",
                (c["slug"], c["title"], c["language"], c["difficulty"], c["topic"],
                 c["statement"], c["starter_code"], c["hint1"], c["hint2"], c["test_json"]))
        conn.execute(
            "INSERT OR IGNORE INTO projects(name,slug) VALUES(?,?)",
            (PROJECT["name"], PROJECT["slug"]))
        pid = conn.execute("SELECT id FROM projects WHERE slug=?", (PROJECT["slug"],)).fetchone()["id"]
        for stage, title in PROJECT["stages"]:
            exists = conn.execute(
                "SELECT 1 FROM project_tasks WHERE project_id=? AND stage=?",
                (pid, stage)).fetchone()
            if not exists:
                conn.execute(
                    "INSERT INTO project_tasks(project_id,stage,title,is_done) VALUES(?,?,?,0)",
                    (pid, stage, title))
        conn.commit()
        print("seed ok")
    finally:
        conn.close()


if __name__ == "__main__":
    seed()
