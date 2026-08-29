import os

from app.core.config import CONTENT_DIR

# ponytail: roadmap manually mirrors belajar.txt top-level structure.
ROADMAP = [
    {
        "name": "Python Fundamentals",
        "phase": "python",
        "topics": [
            {"title": "Variable & Data Types", "lesson": "day01"},
            {"title": "Operators", "lesson": "day02"},
            {"title": "Conditional", "lesson": "day03"},
            {"title": "Loop", "lesson": "day04"},
            {"title": "Function", "lesson": "day05"},
            {"title": "String", "lesson": "day06"},
            {"title": "List", "lesson": "day07"},
            {"title": "Dictionary", "lesson": "day08"},
            {"title": "Set & Tuple", "lesson": "day09"},
        ],
    },
    {
        "name": "Python Intermediate",
        "phase": "python",
        "topics": [
            {"title": "Exception", "lesson": "day10"},
            {"title": "File Handling", "lesson": "day11"},
            {"title": "Module & Package", "lesson": "day12"},
            {"title": "OOP: Class & Object", "lesson": "day13"},
            {"title": "OOP: Inheritance & Poly", "lesson": "day14"},
            {"title": "Typing & Dataclass", "lesson": "day15"},
            {"title": "Decorator", "lesson": "day16"},
            {"title": "Generator", "lesson": "day17"},
            {"title": "Context Manager", "lesson": "day18"},
        ],
    },
    {
        "name": "Python Problem Solving",
        "phase": "python",
        "topics": [
            {"title": "Big-O / Complexity", "lesson": "day19"},
            {"title": "Searching", "lesson": "day20"},
            {"title": "Sorting", "lesson": "day21"},
            {"title": "Data Structures", "lesson": "day22"},
        ],
    },
    {
        "name": "Python Software Engineering",
        "phase": "python",
        "topics": [
            {"title": "Testing (pytest)", "lesson": "day23"},
            {"title": "Git", "lesson": "day24"},
            {"title": "Debugging", "lesson": "day25"},
        ],
    },
    {
        "name": "Python Backend",
        "phase": "python",
        "topics": [
            {"title": "HTTP & REST", "lesson": "day26"},
            {"title": "FastAPI Intro", "lesson": "day27"},
            {"title": "Backend Project (EMP API)", "lesson": "day28"},
        ],
    },
    {
        "name": "Python OOP",
        "phase": "python",
        "topics": [
            {"title": "Class", "lesson": None},
            {"title": "Object", "lesson": None},
            {"title": "Inheritance", "lesson": None},
        ],
    },
    {
        "name": "PHP Fundamentals",
        "phase": "php",
        "topics": [
            {"title": "Syntax & Type", "lesson": None},
            {"title": "Array", "lesson": None},
            {"title": "Function", "lesson": None},
        ],
    },
    {
        "name": "Database & SQL",
        "phase": "sql",
        "topics": [
            {"title": "SELECT / CRUD", "lesson": None},
            {"title": "JOIN", "lesson": None},
            {"title": "Normalization", "lesson": None},
        ],
    },
    {
        "name": "CodeIgniter",
        "phase": "codeigniter",
        "topics": [
            {"title": "Routing", "lesson": None},
            {"title": "Controller & Model", "lesson": None},
            {"title": "Auth", "lesson": None},
        ],
    },
    {
        "name": "Laravel",
        "phase": "laravel",
        "topics": [
            {"title": "Routing & Middleware", "lesson": None},
            {"title": "Eloquent", "lesson": None},
            {"title": "Queue", "lesson": None},
        ],
    },
    {
        "name": "JavaScript",
        "phase": "javascript",
        "topics": [
            {"title": "Types & Functions", "lesson": None},
            {"title": "DOM & Events", "lesson": None},
            {"title": "Async/Await", "lesson": None},
        ],
    },
    {
        "name": "Software Engineering",
        "phase": "se",
        "topics": [
            {"title": "Git", "lesson": None},
            {"title": "Testing", "lesson": None},
            {"title": "Architecture", "lesson": None},
        ],
    },
]


def load_markdown(slug: str) -> str | None:
    for folder in ("daily", "python", "php", "javascript", "database",
                   "software_engineering", "codeigniter", "laravel"):
        path = os.path.join(CONTENT_DIR, folder, f"{slug}.md")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
    return None


def search_index() -> list[dict]:
    # ponytail: index only lessons already present on disk
    items = []
    for folder in os.listdir(CONTENT_DIR):
        fdir = os.path.join(CONTENT_DIR, folder)
        if not os.path.isdir(fdir):
            continue
        for fname in os.listdir(fdir):
            if fname.endswith(".md"):
                slug = os.path.splitext(fname)[0]
                with open(os.path.join(fdir, fname), encoding="utf-8") as f:
                    items.append({"slug": slug, "folder": folder, "title": slug,
                                  "text": f.read()[:2000]})
    return items
