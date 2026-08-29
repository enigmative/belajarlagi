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
    {"slug": "day10", "title": "Day 10 — Exception Handling", "phase": "python", "order": 10, "file": "daily/day10.md"},
    {"slug": "day11", "title": "Day 11 — File Handling", "phase": "python", "order": 11, "file": "daily/day11.md"},
    {"slug": "day12", "title": "Day 12 — Module & Package", "phase": "python", "order": 12, "file": "daily/day12.md"},
    {"slug": "day13", "title": "Day 13 — OOP: Class & Object", "phase": "python", "order": 13, "file": "daily/day13.md"},
    {"slug": "day14", "title": "Day 14 — OOP: Inheritance & Polymorphism", "phase": "python", "order": 14, "file": "daily/day14.md"},
    {"slug": "day15", "title": "Day 15 — Typing & Dataclass", "phase": "python", "order": 15, "file": "daily/day15.md"},
    {"slug": "day16", "title": "Day 16 — Decorator", "phase": "python", "order": 16, "file": "daily/day16.md"},
    {"slug": "day17", "title": "Day 17 — Generator & Iterator", "phase": "python", "order": 17, "file": "daily/day17.md"},
    {"slug": "day18", "title": "Day 18 — Context Manager", "phase": "python", "order": 18, "file": "daily/day18.md"},
    {"slug": "day19", "title": "Day 19 — Big-O & Complexity", "phase": "python", "order": 19, "file": "daily/day19.md"},
    {"slug": "day20", "title": "Day 20 — Searching", "phase": "python", "order": 20, "file": "daily/day20.md"},
    {"slug": "day21", "title": "Day 21 — Sorting", "phase": "python", "order": 21, "file": "daily/day21.md"},
    {"slug": "day22", "title": "Day 22 — Data Structures", "phase": "python", "order": 22, "file": "daily/day22.md"},
    {"slug": "day23", "title": "Day 23 — Testing with pytest", "phase": "python", "order": 23, "file": "daily/day23.md"},
    {"slug": "day24", "title": "Day 24 — Git", "phase": "python", "order": 24, "file": "daily/day24.md"},
    {"slug": "day25", "title": "Day 25 — Debugging", "phase": "python", "order": 25, "file": "daily/day25.md"},
    {"slug": "day26", "title": "Day 26 — HTTP & REST", "phase": "python", "order": 26, "file": "daily/day26.md"},
    {"slug": "day27", "title": "Day 27 — FastAPI", "phase": "python", "order": 27, "file": "daily/day27.md"},
    {"slug": "day28", "title": "Day 28 — Backend Project (Employee API)", "phase": "python", "order": 28, "file": "daily/day28.md"},
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
