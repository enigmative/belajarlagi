"""One-time migration from the old single-user schema to multi-user tables.

The new schema is installed by ``database.schema.sql``. SQLite does not alter
existing tables from ``CREATE TABLE IF NOT EXISTS``, so this module rebuilds the
personal tables and assigns any legacy rows to a locked owner account.
"""
import sqlite3

PERSONAL_TABLES = (
    "lesson_progress",
    "course_enrollments",
    "challenge_attempts",
    "learning_sessions",
    "interview_progress",
    "notes",
    "mistakes",
)


def _table_exists(conn: sqlite3.Connection, table: str) -> bool:
    row = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (table,)
    ).fetchone()
    return row is not None


def _columns(conn: sqlite3.Connection, table: str) -> set[str]:
    return {row[1] for row in conn.execute(f"PRAGMA table_info({table})")}


def _has_personal_data(conn: sqlite3.Connection) -> bool:
    for table in PERSONAL_TABLES:
        if not _table_exists(conn, table):
            continue
        count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        if count:
            return True
    if _table_exists(conn, "project_tasks"):
        done = conn.execute(
            "SELECT COUNT(*) FROM project_tasks WHERE is_done=1"
        ).fetchone()[0]
        if done:
            return True
    return False


def _legacy_owner_id(conn: sqlite3.Connection, has_data: bool) -> int | None:
    if not has_data:
        return None
    row = conn.execute("SELECT id FROM users ORDER BY id LIMIT 1").fetchone()
    if row:
        return row[0]
    cur = conn.execute(
        "INSERT INTO users(email, name, password_hash, role, is_active) "
        "VALUES('owner@local', 'Owner', '!', 'admin', 1)"
    )
    return cur.lastrowid


def _drop_old(conn: sqlite3.Connection, table: str):
    old = f"_legacy_{table}"
    conn.execute(f"DROP TABLE IF EXISTS {old}")
    conn.execute(f"ALTER TABLE {table} RENAME TO {old}")
    return old


def _rebuild_lesson_progress(conn, owner_id):
    old = _drop_old(conn, "lesson_progress")
    conn.execute(
        """
        CREATE TABLE lesson_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            lesson_id INTEGER NOT NULL,
            status TEXT NOT NULL CHECK(status IN ('in_progress','completed')),
            completed_at TEXT,
            answers_json TEXT,
            UNIQUE(user_id, lesson_id),
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY(lesson_id) REFERENCES lessons(id)
        )
        """
    )
    if owner_id is not None:
        conn.execute(
            f"""
            INSERT INTO lesson_progress
                (user_id, lesson_id, status, completed_at, answers_json)
            SELECT ?, lesson_id,
                CASE WHEN MAX(CASE WHEN status='completed' THEN 1 ELSE 0 END)=1
                     THEN 'completed' ELSE 'in_progress' END,
                MAX(completed_at),
                (SELECT o2.answers_json FROM {old} o2
                 WHERE o2.lesson_id=o.lesson_id ORDER BY o2.id DESC LIMIT 1)
            FROM {old} o
            GROUP BY lesson_id
            """,
            (owner_id,),
        )
    conn.execute(f"DROP TABLE {old}")


def _rebuild_course_enrollments(conn, owner_id):
    old = _drop_old(conn, "course_enrollments")
    conn.execute(
        """
        CREATE TABLE course_enrollments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            course_id INTEGER NOT NULL,
            enrolled_at TEXT NOT NULL DEFAULT (datetime('now')),
            last_accessed_at TEXT,
            UNIQUE(user_id, course_id),
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY(course_id) REFERENCES courses(id)
        )
        """
    )
    if owner_id is not None:
        conn.execute(
            f"INSERT INTO course_enrollments"
            f"(user_id, course_id, enrolled_at, last_accessed_at) "
            f"SELECT ?, course_id, enrolled_at, last_accessed_at FROM {old}",
            (owner_id,),
        )
    conn.execute(f"DROP TABLE {old}")


def _rebuild_challenge_attempts(conn, owner_id):
    old = _drop_old(conn, "challenge_attempts")
    conn.execute(
        """
        CREATE TABLE challenge_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            challenge_id INTEGER NOT NULL,
            attempt_number INTEGER NOT NULL,
            result TEXT NOT NULL,
            execution_time REAL,
            hints_used INTEGER DEFAULT 0,
            submitted_at TEXT NOT NULL,
            code TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY(challenge_id) REFERENCES challenges(id)
        )
        """
    )
    if owner_id is not None:
        conn.execute(
            f"INSERT INTO challenge_attempts"
            f"(user_id, challenge_id, attempt_number, result, execution_time, "
            f"hints_used, submitted_at, code) "
            f"SELECT ?, challenge_id, attempt_number, result, execution_time, "
            f"hints_used, submitted_at, code FROM {old}",
            (owner_id,),
        )
    conn.execute(f"DROP TABLE {old}")
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_challenge_attempts_user "
        "ON challenge_attempts(user_id, challenge_id)"
    )


def _rebuild_learning_sessions(conn, owner_id):
    old = _drop_old(conn, "learning_sessions")
    conn.execute(
        """
        CREATE TABLE learning_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            minutes INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """
    )
    if owner_id is not None:
        conn.execute(
            f"INSERT INTO learning_sessions(user_id, date, minutes) "
            f"SELECT ?, date, minutes FROM {old}",
            (owner_id,),
        )
    conn.execute(f"DROP TABLE {old}")
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_learning_sessions_user "
        "ON learning_sessions(user_id, date)"
    )


def _rebuild_interview_progress(conn, owner_id):
    old = _drop_old(conn, "interview_progress")
    conn.execute(
        """
        CREATE TABLE interview_progress (
            user_id INTEGER NOT NULL,
            question_id TEXT NOT NULL,
            status TEXT NOT NULL CHECK(status IN ('unseen','wrong','correct')),
            attempts INTEGER NOT NULL DEFAULT 0,
            last_choice TEXT,
            updated_at TEXT NOT NULL DEFAULT (datetime('now')),
            PRIMARY KEY(user_id, question_id),
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """
    )
    if owner_id is not None:
        conn.execute(
            f"INSERT INTO interview_progress"
            f"(user_id, question_id, status, attempts, last_choice, updated_at) "
            f"SELECT ?, question_id, status, attempts, last_choice, updated_at FROM {old}",
            (owner_id,),
        )
    conn.execute(f"DROP TABLE {old}")


def _rebuild_simple_user_table(conn, table: str, owner_id, columns: str, create_sql: str):
    old = _drop_old(conn, table)
    conn.execute(create_sql)
    if owner_id is not None:
        conn.execute(
            f"INSERT INTO {table}(user_id, {columns}) "
            f"SELECT ?, {columns} FROM {old}",
            (owner_id,),
        )
    conn.execute(f"DROP TABLE {old}")


def _ensure_project_task_progress(conn: sqlite3.Connection):
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS project_task_progress (
            user_id INTEGER NOT NULL,
            task_id INTEGER NOT NULL,
            is_done INTEGER NOT NULL DEFAULT 0,
            updated_at TEXT NOT NULL DEFAULT (datetime('now')),
            PRIMARY KEY(user_id, task_id),
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY(task_id) REFERENCES project_tasks(id) ON DELETE CASCADE
        )
        """
    )


def ensure_indexes(conn: sqlite3.Connection):
    statements = (
        "CREATE INDEX IF NOT EXISTS idx_challenge_attempts_user "
        "ON challenge_attempts(user_id, challenge_id)",
        "CREATE INDEX IF NOT EXISTS idx_learning_sessions_user "
        "ON learning_sessions(user_id, date)",
        "CREATE INDEX IF NOT EXISTS idx_notes_user ON notes(user_id, id)",
        "CREATE INDEX IF NOT EXISTS idx_mistakes_user ON mistakes(user_id, id)",
    )
    for statement in statements:
        conn.execute(statement)
    conn.commit()


def migrate_multi_user(conn: sqlite3.Connection):
    """Rebuild legacy personal tables when they do not have user_id yet."""
    if not _table_exists(conn, "lesson_progress"):
        return
    missing = [
        table for table in PERSONAL_TABLES
        if _table_exists(conn, table) and "user_id" not in _columns(conn, table)
    ]
    if not missing:
        return

    has_data = _has_personal_data(conn)
    owner_id = _legacy_owner_id(conn, has_data)
    conn.commit()
    conn.execute("PRAGMA foreign_keys = OFF")
    try:
        conn.execute("BEGIN IMMEDIATE")
        if "lesson_progress" in missing:
            _rebuild_lesson_progress(conn, owner_id)
        if "course_enrollments" in missing:
            _rebuild_course_enrollments(conn, owner_id)
        if "challenge_attempts" in missing:
            _rebuild_challenge_attempts(conn, owner_id)
        if "learning_sessions" in missing:
            _rebuild_learning_sessions(conn, owner_id)
        if "interview_progress" in missing:
            _rebuild_interview_progress(conn, owner_id)
        if "notes" in missing:
            _rebuild_simple_user_table(
                conn, "notes", owner_id, "title, body, kind, created_at",
                """
                CREATE TABLE notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    body TEXT NOT NULL,
                    kind TEXT DEFAULT 'concept',
                    created_at TEXT NOT NULL,
                    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
                )
                """,
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_notes_user ON notes(user_id, id)"
            )
        if "mistakes" in missing:
            _rebuild_simple_user_table(
                conn, "mistakes", owner_id, "problem, cause, lesson, prevention, created_at",
                """
                CREATE TABLE mistakes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    problem TEXT NOT NULL,
                    cause TEXT,
                    lesson TEXT,
                    prevention TEXT,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
                )
                """,
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_mistakes_user "
                "ON mistakes(user_id, id)"
            )
        # Preserve the old global project checklist as the owner's checklist.
        if owner_id is not None and _table_exists(conn, "project_tasks"):
            _ensure_project_task_progress(conn)
            conn.execute(
                "INSERT OR IGNORE INTO project_task_progress"
                "(user_id, task_id, is_done, updated_at) "
                "SELECT ?, id, 1, datetime('now') FROM project_tasks WHERE is_done=1",
                (owner_id,),
            )
            conn.execute("UPDATE project_tasks SET is_done=0")
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.execute("PRAGMA foreign_keys = ON")
