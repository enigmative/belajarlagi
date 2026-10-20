"""Migration test for the old single-user SQLite schema."""
import sqlite3

from database.migrations import ensure_indexes, migrate_multi_user


def _old_db():
    conn = sqlite3.connect(":memory:")
    conn.executescript(
        """
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE COLLATE NOCASE,
            name TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user',
            is_active INTEGER NOT NULL DEFAULT 1,
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            last_login_at TEXT
        );
        CREATE TABLE lessons (id INTEGER PRIMARY KEY, slug TEXT, title TEXT);
        INSERT INTO lessons(id, slug, title) VALUES (1, 'day01', 'Day 01');
        CREATE TABLE courses (id INTEGER PRIMARY KEY, slug TEXT, title TEXT);
        INSERT INTO courses(id, slug, title) VALUES (1, 'python', 'Python');
        CREATE TABLE challenges (id INTEGER PRIMARY KEY, slug TEXT);
        INSERT INTO challenges(id, slug) VALUES (1, 'fizzbuzz');
        CREATE TABLE projects (id INTEGER PRIMARY KEY, name TEXT, slug TEXT);
        INSERT INTO projects(id, name, slug) VALUES (1, 'Project', 'project');
        CREATE TABLE project_tasks (
            id INTEGER PRIMARY KEY, project_id INTEGER, stage TEXT, title TEXT,
            is_done INTEGER DEFAULT 0
        );
        INSERT INTO project_tasks(id, project_id, stage, title, is_done)
            VALUES (1, 1, 'Stage', 'Task', 1);

        CREATE TABLE lesson_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT, lesson_id INTEGER, status TEXT,
            completed_at TEXT, answers_json TEXT
        );
        INSERT INTO lesson_progress(lesson_id, status, completed_at, answers_json)
            VALUES (1, 'in_progress', NULL, '{}');
        INSERT INTO lesson_progress(lesson_id, status, completed_at, answers_json)
            VALUES (1, 'completed', '2026-01-01 00:00:00', '{"a":1}');

        CREATE TABLE course_enrollments (
            id INTEGER PRIMARY KEY AUTOINCREMENT, course_id INTEGER,
            enrolled_at TEXT, last_accessed_at TEXT
        );
        INSERT INTO course_enrollments(course_id, enrolled_at)
            VALUES (1, '2026-01-01 00:00:00');

        CREATE TABLE challenge_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT, challenge_id INTEGER,
            attempt_number INTEGER, result TEXT, execution_time REAL,
            hints_used INTEGER, submitted_at TEXT, code TEXT
        );
        INSERT INTO challenge_attempts
            (challenge_id, attempt_number, result, submitted_at)
            VALUES (1, 1, 'failed', '2026-01-01 00:00:00');
        INSERT INTO challenge_attempts
            (challenge_id, attempt_number, result, submitted_at)
            VALUES (1, 2, 'passed', '2026-01-01 00:01:00');

        CREATE TABLE learning_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, minutes INTEGER
        );
        INSERT INTO learning_sessions(date, minutes) VALUES ('2026-01-01', 20);

        CREATE TABLE interview_progress (
            question_id TEXT PRIMARY KEY, status TEXT, attempts INTEGER,
            last_choice TEXT, updated_at TEXT
        );
        INSERT INTO interview_progress
            (question_id, status, attempts, updated_at)
            VALUES ('q1', 'correct', 1, '2026-01-01 00:00:00');

        CREATE TABLE notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, body TEXT,
            kind TEXT, created_at TEXT
        );
        INSERT INTO notes(title, body, created_at) VALUES ('n', 'b', '2026-01-01');

        CREATE TABLE mistakes (
            id INTEGER PRIMARY KEY AUTOINCREMENT, problem TEXT, cause TEXT,
            lesson TEXT, prevention TEXT, created_at TEXT
        );
        INSERT INTO mistakes(problem, created_at) VALUES ('p', '2026-01-01');
        """
    )
    return conn


def test_migrates_old_personal_tables_to_owner_account():
    conn = _old_db()
    try:
        migrate_multi_user(conn)
        ensure_indexes(conn)

        owner = conn.execute("SELECT * FROM users").fetchone()
        assert owner[1] == "owner@local"
        assert owner[4] == "admin"
        assert owner[3] == "!"

        progress = conn.execute("SELECT * FROM lesson_progress").fetchall()
        assert len(progress) == 1
        assert progress[0][1] == owner[0]
        assert progress[0][3] == "completed"

        assert conn.execute("SELECT COUNT(*) FROM course_enrollments").fetchone()[0] == 1
        assert conn.execute("SELECT COUNT(*) FROM challenge_attempts").fetchone()[0] == 2
        assert conn.execute("SELECT COUNT(*) FROM learning_sessions").fetchone()[0] == 1
        assert conn.execute("SELECT COUNT(*) FROM interview_progress").fetchone()[0] == 1
        assert conn.execute("SELECT COUNT(*) FROM notes").fetchone()[0] == 1
        assert conn.execute("SELECT COUNT(*) FROM mistakes").fetchone()[0] == 1

        done = conn.execute(
            "SELECT is_done FROM project_task_progress WHERE user_id=? AND task_id=1",
            (owner[0],),
        ).fetchone()
        assert done[0] == 1
        assert conn.execute("SELECT is_done FROM project_tasks WHERE id=1").fetchone()[0] == 0

        columns = {row[1] for row in conn.execute("PRAGMA table_info(lesson_progress)")}
        assert "user_id" in columns
    finally:
        conn.close()
