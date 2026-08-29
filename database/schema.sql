-- Belajar Lagi — SQLite schema
-- ponytail: single simple schema, matches master prompt section 38.

CREATE TABLE IF NOT EXISTS phases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    order_index INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS lessons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    phase_slug TEXT NOT NULL,
    order_index INTEGER NOT NULL,
    content_file TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS lesson_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lesson_id INTEGER NOT NULL,
    status TEXT NOT NULL CHECK(status IN ('in_progress','completed')),
    completed_at TEXT,
    answers_json TEXT,
    FOREIGN KEY(lesson_id) REFERENCES lessons(id)
);

CREATE TABLE IF NOT EXISTS challenges (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    language TEXT NOT NULL,
    difficulty TEXT NOT NULL,
    topic TEXT,
    statement TEXT NOT NULL,
    starter_code TEXT,
    hint1 TEXT,
    hint2 TEXT,
    test_json TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS challenge_attempts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    challenge_id INTEGER NOT NULL,
    attempt_number INTEGER NOT NULL,
    result TEXT NOT NULL,
    execution_time REAL,
    hints_used INTEGER DEFAULT 0,
    submitted_at TEXT NOT NULL,
    code TEXT,
    FOREIGN KEY(challenge_id) REFERENCES challenges(id)
);

CREATE TABLE IF NOT EXISTS learning_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    minutes INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    kind TEXT DEFAULT 'concept',
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS mistakes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    problem TEXT NOT NULL,
    cause TEXT,
    lesson TEXT,
    prevention TEXT,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    slug TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS project_tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    stage TEXT NOT NULL,
    title TEXT NOT NULL,
    is_done INTEGER DEFAULT 0,
    FOREIGN KEY(project_id) REFERENCES projects(id)
);
