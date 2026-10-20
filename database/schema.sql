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

-- Course catalogue: Course -> Module -> Lesson.
-- lessons stay as-is so existing progress and Markdown files keep working.
CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    category TEXT,
    level TEXT,
    icon TEXT,
    order_index INTEGER NOT NULL DEFAULT 0,
    is_published INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS course_modules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER NOT NULL,
    slug TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    order_index INTEGER NOT NULL DEFAULT 0,
    UNIQUE(course_id, slug),
    FOREIGN KEY(course_id) REFERENCES courses(id)
);

CREATE TABLE IF NOT EXISTS course_lessons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER NOT NULL,
    module_id INTEGER,
    lesson_id INTEGER NOT NULL,
    order_index INTEGER NOT NULL DEFAULT 0,
    UNIQUE(course_id, lesson_id),
    FOREIGN KEY(course_id) REFERENCES courses(id),
    FOREIGN KEY(module_id) REFERENCES course_modules(id),
    FOREIGN KEY(lesson_id) REFERENCES lessons(id)
);

CREATE TABLE IF NOT EXISTS course_enrollments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER NOT NULL UNIQUE,
    enrolled_at TEXT NOT NULL DEFAULT (datetime('now')),
    last_accessed_at TEXT,
    FOREIGN KEY(course_id) REFERENCES courses(id)
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

-- Interview Prep: status per soal (unseen / wrong / correct)
CREATE TABLE IF NOT EXISTS interview_progress (
    question_id TEXT PRIMARY KEY,
    status TEXT NOT NULL CHECK(status IN ('unseen','wrong','correct')),
    attempts INTEGER NOT NULL DEFAULT 0,
    last_choice TEXT,
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
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
