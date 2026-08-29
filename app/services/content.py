import os

from app.core.config import CONTENT_DIR

# ponytail: roadmap manually mirrors belajar.txt top-level structure.
ROADMAP = [
    {
        "name": "Python Fundamentals",
        "phase": "python",
        "topics": [
            {"title": "Variable & Data Types", "lesson": "day01"},
            {"title": "Operators", "lesson": None},
            {"title": "Conditional", "lesson": None},
            {"title": "Loop", "lesson": None},
            {"title": "Function", "lesson": None},
        ],
    },
    {
        "name": "Python Problem Solving",
        "phase": "python",
        "topics": [
            {"title": "Searching", "lesson": None},
            {"title": "Sorting", "lesson": None},
            {"title": "Hash Map", "lesson": None},
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
