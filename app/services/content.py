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
            {"title": "Class", "lesson": "day13"},
            {"title": "Object", "lesson": "day13"},
            {"title": "Inheritance", "lesson": "day14"},
        ],
    },
    {
        "name": "Database & SQL",
        "phase": "sql",
        "topics": [
            {"title": "SELECT / CRUD", "lesson": "sql-crud"},
            {"title": "JOIN", "lesson": "sql-join"},
            {"title": "Design & Normalization", "lesson": "sql-design"},
            {"title": "Transaction", "lesson": "sql-transaction"},
            {"title": "Query Optimization", "lesson": "sql-optimization"},
        ],
    },
    {
        "name": "PHP Fundamentals",
        "phase": "php",
        "topics": [
            {"title": "Syntax & Type", "lesson": "php-basics"},
            {"title": "Function & Array", "lesson": "php-functions"},
            {"title": "OOP", "lesson": "php-oop"},
            {"title": "Composer, PSR & SOLID", "lesson": "php-composer"},
        ],
    },
    {
        "name": "CodeIgniter",
        "phase": "codeigniter",
        "topics": [
            {"title": "MVC & Routing", "lesson": "ci-mvc-routing"},
            {"title": "Model & Database", "lesson": "ci-model-db"},
            {"title": "Auth, Filter & REST", "lesson": "ci-auth-rest"},
        ],
    },
    {
        "name": "Laravel",
        "phase": "laravel",
        "topics": [
            {"title": "Routing, Controller & Blade", "lesson": "laravel-basics"},
            {"title": "Eloquent & Relasi", "lesson": "laravel-eloquent"},
            {"title": "Auth, Queue & Events", "lesson": "laravel-advanced"},
        ],
    },
    {
        "name": "JavaScript",
        "phase": "javascript",
        "topics": [
            {"title": "Types & Functions", "lesson": "js-basics"},
            {"title": "DOM & Events", "lesson": "js-dom"},
            {"title": "Async/Await & Fetch", "lesson": "js-async"},
            {"title": "Frontend Framework", "lesson": "js-framework"},
        ],
    },
    {
        "name": "Web Security",
        "phase": "se",
        "topics": [
            {"title": "Auth, Session & Password", "lesson": "sec-auth"},
            {"title": "CSRF, XSS & SQLi", "lesson": "sec-attacks"},
            {"title": "API Hardening", "lesson": "sec-api"},
        ],
    },
    {
        "name": "Docker",
        "phase": "se",
        "topics": [
            {"title": "Image & Container", "lesson": "docker-basics"},
            {"title": "Volume, Network & Compose", "lesson": "docker-compose"},
        ],
    },
    {
        "name": "Linux",
        "phase": "se",
        "topics": [
            {"title": "Command Line", "lesson": "linux-basics"},
            {"title": "Process, Port & Resources", "lesson": "linux-process"},
            {"title": "Service, Logs & Environment", "lesson": "linux-service-logs"},
        ],
    },
    {
        "name": "Redis & Queue",
        "phase": "se",
        "topics": [
            {"title": "Caching & Session", "lesson": "redis-cache"},
            {"title": "Queue, Job & Worker", "lesson": "queue-worker"},
        ],
    },
    {
        "name": "CI/CD",
        "phase": "se",
        "topics": [
            {"title": "CI: Build & Test", "lesson": "cicd-build-test"},
            {"title": "CD: Deploy & Rollback", "lesson": "cicd-deploy-rollback"},
        ],
    },
    {
        "name": "Software Architecture",
        "phase": "se",
        "topics": [
            {"title": "MVC, Layered & SOLID", "lesson": "arch-layering"},
            {"title": "Clean Architecture & DI", "lesson": "arch-clean-di"},
        ],
    },
    {
        "name": "System Design",
        "phase": "se",
        "topics": [
            {"title": "Komponen & Arsitektur 3-Tier", "lesson": "system-design-basics"},
            {"title": "Scaling, Replication & Availability", "lesson": "system-design-scaling"},
        ],
    },
    {
        "name": "Observability",
        "phase": "se",
        "topics": [
            {"title": "Structured Logging & Metrics", "lesson": "obs-logging-metrics"},
            {"title": "Tracing, Monitoring & Alerting", "lesson": "obs-tracing-alerts"},
        ],
    },
    {
        "name": "Interview Prep — Sprint 3 Hari",
        "phase": "interview",
        "topics": [
            {"title": "Day 1 — Java & Membaca Kode", "lesson": "interview-day1"},
            {"title": "Day 2 — Spring Boot & JavaScript", "lesson": "interview-day2"},
            {"title": "Day 3 — React, Live Coding & Interview", "lesson": "interview-day3"},
        ],
    },
]


def load_markdown(slug: str) -> str | None:
    for folder in ("daily", "python", "php", "javascript", "database",
                   "software_engineering", "codeigniter", "laravel", "interview"):
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
