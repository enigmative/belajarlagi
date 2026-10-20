import sqlite3
from typing import Any

from database.database import DB_PATH, get_conn


def _rows(q: str, p: tuple = ()) -> list[dict]:
    conn = get_conn()
    try:
        return [dict(r) for r in conn.execute(q, p).fetchall()]
    finally:
        conn.close()


def _one(q: str, p: tuple = ()) -> dict | None:
    rows = _rows(q, p)
    return rows[0] if rows else None


def _exec(q: str, p: tuple = ()) -> int:
    conn = get_conn()
    try:
        cur = conn.execute(q, p)
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()


def _execmany(q: str, seq: list[tuple]):
    conn = get_conn()
    try:
        conn.executemany(q, seq)
        conn.commit()
    finally:
        conn.close()


# ---------- users / auth ----------

def get_user_by_email(email: str):
    return _one("SELECT * FROM users WHERE email=? COLLATE NOCASE", (email,))


def get_user_by_id(user_id: int):
    return _one("SELECT * FROM users WHERE id=?", (user_id,))


def create_user(email: str, name: str, password_hash: str, role: str = "user"):
    return _exec(
        "INSERT INTO users(email, name, password_hash, role) VALUES(?,?,?,?)",
        (email, name, password_hash, role),
    )


def update_user(user_id: int, email: str, name: str, role: str, password_hash: str | None = None):
    if password_hash:
        _exec(
            "UPDATE users SET email=?, name=?, role=?, password_hash=?, is_active=1 WHERE id=?",
            (email, name, role, password_hash, user_id),
        )
    else:
        _exec(
            "UPDATE users SET email=?, name=?, role=?, is_active=1 WHERE id=?",
            (email, name, role, user_id),
        )


def list_users():
    return _rows("SELECT id, email, name, role, is_active, created_at, last_login_at "
                 "FROM users ORDER BY id")


def set_user_password(user_id: int, password_hash: str):
    _exec("UPDATE users SET password_hash=? WHERE id=?", (password_hash, user_id))


def set_user_active(user_id: int, active: bool):
    _exec("UPDATE users SET is_active=? WHERE id=?", (1 if active else 0, user_id))


def mark_user_login(user_id: int):
    _exec("UPDATE users SET last_login_at=datetime('now') WHERE id=?", (user_id,))


def create_auth_session(user_id: int, token_hash: str, days: int = 30):
    _exec(
        "INSERT INTO auth_sessions(user_id, token_hash, expires_at) "
        "VALUES(?,?,datetime('now', ?))",
        (user_id, token_hash, f"+{int(days)} days"),
    )


def user_for_session_token(token_hash: str):
    return _one(
        "SELECT u.* FROM auth_sessions s "
        "JOIN users u ON u.id=s.user_id "
        "WHERE s.token_hash=? AND s.expires_at > datetime('now') AND u.is_active=1",
        (token_hash,),
    )


def delete_auth_session(token_hash: str):
    _exec("DELETE FROM auth_sessions WHERE token_hash=?", (token_hash,))


def delete_user_sessions(user_id: int):
    _exec("DELETE FROM auth_sessions WHERE user_id=?", (user_id,))


def prune_auth_sessions():
    _exec("DELETE FROM auth_sessions WHERE expires_at <= datetime('now')")


def get_legacy_owner():
    return _one("SELECT * FROM users WHERE email='owner@local'")


# ---------- lessons ----------

def get_lessons():
    return _rows(
        "SELECT l.* FROM lessons l "
        "LEFT JOIN phases p ON p.slug = l.phase_slug "
        "ORDER BY COALESCE(p.order_index, 999), l.order_index, l.id"
    )


def get_lesson(slug: str):
    return _one("SELECT * FROM lessons WHERE slug=?", (slug,))


def get_progress(user_id: int, lesson_id: int):
    return _one(
        "SELECT * FROM lesson_progress WHERE user_id=? AND lesson_id=? "
        "ORDER BY id DESC",
        (user_id, lesson_id),
    )


def mark_complete(user_id: int, lesson_id: int):
    conn = get_conn()
    try:
        cur = conn.execute(
            "INSERT INTO lesson_progress(user_id, lesson_id, status, completed_at) "
            "VALUES(?, ?, 'completed', datetime('now')) "
            "ON CONFLICT(user_id, lesson_id) DO UPDATE SET "
            "status='completed', "
            "completed_at=COALESCE(lesson_progress.completed_at, excluded.completed_at)",
            (user_id, lesson_id),
        )
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()


def total_lessons() -> int:
    row = _one("SELECT COUNT(*) AS c FROM lessons")
    return row["c"]


def completed_lessons(user_id: int) -> int:
    row = _one(
        "SELECT COUNT(DISTINCT lesson_id) AS c FROM lesson_progress "
        "WHERE user_id=? AND status='completed'",
        (user_id,),
    )
    return row["c"]


def completed_lesson_ids(user_id: int) -> set:
    rows = _rows(
        "SELECT DISTINCT lesson_id FROM lesson_progress "
        "WHERE user_id=? AND status='completed'",
        (user_id,),
    )
    return {r["lesson_id"] for r in rows}


# ---------- courses ----------

_COURSE_SELECT = (
    "SELECT c.*, "
    "COUNT(DISTINCT cl.lesson_id) AS lessons_total, "
    "COUNT(DISTINCT lp.lesson_id) AS lessons_completed, "
    "CASE WHEN ce.id IS NULL AND lp.lesson_id IS NULL THEN 0 ELSE 1 END AS enrolled "
    "FROM courses c "
    "LEFT JOIN course_lessons cl ON cl.course_id = c.id "
    "LEFT JOIN (SELECT DISTINCT lesson_id FROM lesson_progress "
    "           WHERE status='completed' AND user_id=?) lp "
    "ON lp.lesson_id = cl.lesson_id "
    "LEFT JOIN course_enrollments ce ON ce.course_id = c.id AND ce.user_id=? "
)


def all_courses(user_id: int, enrolled_only: bool = False):
    rows = _rows(
        _COURSE_SELECT
        + " WHERE c.is_published=1 GROUP BY c.id ORDER BY c.order_index, c.id",
        (user_id, user_id),
    )
    if enrolled_only:
        return [r for r in rows if r["enrolled"]]
    return rows


def get_course(user_id: int, slug: str):
    return _one(
        _COURSE_SELECT
        + " WHERE c.slug=? AND c.is_published=1 GROUP BY c.id",
        (user_id, user_id, slug),
    )


def course_modules(course_id: int):
    return _rows(
        "SELECT * FROM course_modules WHERE course_id=? ORDER BY order_index, id",
        (course_id,),
    )


def course_lessons(user_id: int, course_id: int):
    return _rows(
        "SELECT cl.order_index AS course_order, cl.module_id, "
        "l.id, l.slug, l.title, l.phase_slug, l.order_index AS lesson_order, "
        "CASE WHEN lp.lesson_id IS NULL THEN 0 ELSE 1 END AS completed "
        "FROM course_lessons cl "
        "JOIN lessons l ON l.id = cl.lesson_id "
        "LEFT JOIN (SELECT DISTINCT lesson_id FROM lesson_progress "
        "           WHERE status='completed' AND user_id=?) lp "
        "ON lp.lesson_id = l.id "
        "WHERE cl.course_id=? ORDER BY cl.order_index, l.id",
        (user_id, course_id),
    )


def course_for_lesson(lesson_id: int):
    return _one(
        "SELECT c.id, c.slug, c.title, c.icon, c.category, c.level, "
        "cm.slug AS module_slug, cm.title AS module_title, cm.id AS module_id "
        "FROM course_lessons cl "
        "JOIN courses c ON c.id = cl.course_id "
        "LEFT JOIN course_modules cm ON cm.id = cl.module_id "
        "WHERE cl.lesson_id=? ORDER BY c.order_index LIMIT 1",
        (lesson_id,),
    )


def course_enrollment(user_id: int, course_id: int):
    return _one(
        "SELECT * FROM course_enrollments WHERE user_id=? AND course_id=?",
        (user_id, course_id),
    )


def enroll_course(user_id: int, course_id: int):
    _exec(
        "INSERT INTO course_enrollments(user_id, course_id, enrolled_at, last_accessed_at) "
        "VALUES(?,?,datetime('now'),datetime('now')) "
        "ON CONFLICT(user_id, course_id) DO UPDATE SET last_accessed_at=datetime('now')",
        (user_id, course_id),
    )


def touch_course_access_for_lesson(user_id: int, lesson_id: int):
    _exec(
        "UPDATE course_enrollments SET last_accessed_at=datetime('now') "
        "WHERE user_id=? AND course_id IN "
        "(SELECT course_id FROM course_lessons WHERE lesson_id=?)",
        (user_id, lesson_id),
    )


# ---------- challenges ----------

def all_challenges():
    return _rows("SELECT * FROM challenges ORDER BY id")


def get_challenge(slug: str):
    return _one("SELECT * FROM challenges WHERE slug=?", (slug,))


def challenge_stats(user_id: int, challenge_id: int):
    return _one(
        "SELECT COUNT(*) AS attempts, "
        "SUM(CASE WHEN result='passed' THEN 1 ELSE 0 END) AS passed, "
        "COALESCE(SUM(hints_used),0) AS hints "
        "FROM challenge_attempts WHERE user_id=? AND challenge_id=?",
        (user_id, challenge_id),
    )


def passed_challenges_count(user_id: int) -> int:
    row = _one(
        "SELECT COUNT(DISTINCT challenge_id) AS c FROM challenge_attempts "
        "WHERE user_id=? AND result='passed'",
        (user_id,),
    )
    return row["c"]


def add_attempt(user_id, challenge_id, attempt_number, result, execution_time, hints_used, code):
    _exec(
        "INSERT INTO challenge_attempts(user_id, challenge_id, attempt_number, result, "
        "execution_time, hints_used, submitted_at, code) "
        "VALUES(?,?,?,?,?,?,datetime('now'),?)",
        (user_id, challenge_id, attempt_number, result, execution_time, hints_used, code),
    )


# ---------- learning sessions (streak) ----------

def touch_session(user_id: int, date: str, minutes: int = 20):
    _exec(
        "INSERT INTO learning_sessions(user_id, date, minutes) VALUES(?,?,?)",
        (user_id, date, minutes),
    )


def learning_minutes(user_id: int) -> int:
    row = _one(
        "SELECT COALESCE(SUM(minutes),0) AS m FROM learning_sessions WHERE user_id=?",
        (user_id,),
    )
    return row["m"]


def distinct_dates(user_id: int):
    return [
        r["date"]
        for r in _rows(
            "SELECT DISTINCT date FROM learning_sessions WHERE user_id=?",
            (user_id,),
        )
    ]


# ---------- interview prep ----------

def interview_progress_all(user_id: int) -> dict:
    rows = _rows("SELECT * FROM interview_progress WHERE user_id=?", (user_id,))
    return {r["question_id"]: r for r in rows}


def interview_progress(user_id: int, question_id: str):
    return _one(
        "SELECT * FROM interview_progress WHERE user_id=? AND question_id=?",
        (user_id, question_id),
    )


def set_interview_status(user_id: int, question_id: str, status: str, choice: str | None = None):
    _exec(
        "INSERT INTO interview_progress"
        "(user_id, question_id, status, attempts, last_choice, updated_at) "
        "VALUES(?,?,?,1,?,datetime('now')) "
        "ON CONFLICT(user_id, question_id) DO UPDATE SET "
        "status=excluded.status, "
        "attempts=interview_progress.attempts + 1, "
        "last_choice=COALESCE(excluded.last_choice, interview_progress.last_choice), "
        "updated_at=excluded.updated_at",
        (user_id, question_id, status, choice),
    )


def reset_interview_status(user_id: int, question_id: str):
    _exec(
        "DELETE FROM interview_progress WHERE user_id=? AND question_id=?",
        (user_id, question_id),
    )


# ---------- notes / mistakes ----------

def list_notes(user_id: int):
    return _rows("SELECT * FROM notes WHERE user_id=? ORDER BY id DESC", (user_id,))


def add_note(user_id: int, title, body, kind):
    return _exec(
        "INSERT INTO notes(user_id, title, body, kind, created_at) "
        "VALUES(?,?,?,?,datetime('now'))",
        (user_id, title, body, kind),
    )


def del_note(user_id: int, note_id):
    _exec("DELETE FROM notes WHERE id=? AND user_id=?", (note_id, user_id))


def list_mistakes(user_id: int):
    return _rows("SELECT * FROM mistakes WHERE user_id=? ORDER BY id DESC", (user_id,))


def add_mistake(user_id: int, problem, cause, lesson, prevention):
    return _exec(
        "INSERT INTO mistakes(user_id, problem, cause, lesson, prevention, created_at) "
        "VALUES(?,?,?,?,?,datetime('now'))",
        (user_id, problem, cause, lesson, prevention),
    )


def del_mistake(user_id: int, mistake_id):
    _exec("DELETE FROM mistakes WHERE id=? AND user_id=?", (mistake_id, user_id))


# ---------- projects ----------

def get_projects():
    return _rows("SELECT * FROM projects ORDER BY id")


def project_stages(user_id: int, project_id):
    return _rows(
        "SELECT pt.id, pt.project_id, pt.stage, pt.title, "
        "COALESCE(ptp.is_done,0) AS is_done "
        "FROM project_tasks pt "
        "LEFT JOIN project_task_progress ptp "
        "ON ptp.task_id = pt.id AND ptp.user_id=? "
        "WHERE pt.project_id=? ORDER BY pt.id",
        (user_id, project_id),
    )


def toggle_project_task(user_id: int, project_slug: str, task_id: int, is_done: bool) -> bool:
    task = _one(
        "SELECT pt.id FROM project_tasks pt "
        "JOIN projects p ON p.id=pt.project_id "
        "WHERE pt.id=? AND p.slug=?",
        (task_id, project_slug),
    )
    if not task:
        return False
    _exec(
        "INSERT INTO project_task_progress(user_id, task_id, is_done, updated_at) "
        "VALUES(?,?,?,datetime('now')) "
        "ON CONFLICT(user_id, task_id) DO UPDATE SET "
        "is_done=excluded.is_done, updated_at=excluded.updated_at",
        (user_id, task_id, 1 if is_done else 0),
    )
    return True
