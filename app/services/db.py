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


# ---------- lessons ----------

def get_lessons():
    return _rows(
        "SELECT l.* FROM lessons l "
        "LEFT JOIN phases p ON p.slug = l.phase_slug "
        "ORDER BY COALESCE(p.order_index, 999), l.order_index, l.id"
    )


def get_lesson(slug: str):
    return _one("SELECT * FROM lessons WHERE slug=?", (slug,))


def get_progress(lesson_id: int):
    return _one(
        "SELECT * FROM lesson_progress WHERE lesson_id=? ORDER BY id DESC",
        (lesson_id,),
    )


def mark_complete(lesson_id: int):
    conn = get_conn()
    try:
        cur = conn.execute(
            "INSERT INTO lesson_progress(lesson_id, status, completed_at) "
            "VALUES(?, 'completed', datetime('now'))",
            (lesson_id,),
        )
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()


def total_lessons() -> int:
    row = _one("SELECT COUNT(*) AS c FROM lessons")
    return row["c"]


def completed_lessons() -> int:
    row = _one(
        "SELECT COUNT(DISTINCT lesson_id) AS c FROM lesson_progress "
        "WHERE status='completed'"
    )
    return row["c"]


def completed_lesson_ids() -> set:
    rows = _rows("SELECT DISTINCT lesson_id FROM lesson_progress WHERE status='completed'")
    return {r["lesson_id"] for r in rows}


# ---------- courses ----------

_COURSE_SELECT = (
    "SELECT c.*, "
    "COUNT(DISTINCT cl.lesson_id) AS lessons_total, "
    "COUNT(DISTINCT lp.lesson_id) AS lessons_completed, "
    "CASE WHEN ce.id IS NULL AND lp.lesson_id IS NULL THEN 0 ELSE 1 END AS enrolled "
    "FROM courses c "
    "LEFT JOIN course_lessons cl ON cl.course_id = c.id "
    "LEFT JOIN (SELECT DISTINCT lesson_id FROM lesson_progress WHERE status='completed') lp "
    "ON lp.lesson_id = cl.lesson_id "
    "LEFT JOIN course_enrollments ce ON ce.course_id = c.id "
)


def all_courses(enrolled_only: bool = False):
    where = "WHERE c.is_published=1"
    if enrolled_only:
        where += (
            " AND (EXISTS(SELECT 1 FROM course_enrollments ce2 WHERE ce2.course_id=c.id)"
            " OR EXISTS(SELECT 1 FROM course_lessons cl2"
            " JOIN lesson_progress lp2 ON lp2.lesson_id=cl2.lesson_id"
            " WHERE cl2.course_id=c.id AND lp2.status='completed'))"
        )
    return _rows(
        _COURSE_SELECT
        + where
        + " GROUP BY c.id ORDER BY c.order_index, c.id"
    )


def get_course(slug: str):
    return _one(
        _COURSE_SELECT
        + " WHERE c.slug=? AND c.is_published=1 GROUP BY c.id",
        (slug,),
    )


def course_modules(course_id: int):
    return _rows(
        "SELECT * FROM course_modules WHERE course_id=? ORDER BY order_index, id",
        (course_id,),
    )


def course_lessons(course_id: int):
    return _rows(
        "SELECT cl.order_index AS course_order, cl.module_id, "
        "l.id, l.slug, l.title, l.phase_slug, l.order_index AS lesson_order, "
        "CASE WHEN lp.lesson_id IS NULL THEN 0 ELSE 1 END AS completed "
        "FROM course_lessons cl "
        "JOIN lessons l ON l.id = cl.lesson_id "
        "LEFT JOIN (SELECT DISTINCT lesson_id FROM lesson_progress WHERE status='completed') lp "
        "ON lp.lesson_id = l.id "
        "WHERE cl.course_id=? ORDER BY cl.order_index, l.id",
        (course_id,),
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


def course_enrollment(course_id: int):
    return _one("SELECT * FROM course_enrollments WHERE course_id=?", (course_id,))


def enroll_course(course_id: int):
    _exec(
        "INSERT INTO course_enrollments(course_id,enrolled_at,last_accessed_at) "
        "VALUES(?,datetime('now'),datetime('now')) "
        "ON CONFLICT(course_id) DO UPDATE SET last_accessed_at=datetime('now')",
        (course_id,),
    )


def touch_course_access_for_lesson(lesson_id: int):
    _exec(
        "UPDATE course_enrollments SET last_accessed_at=datetime('now') "
        "WHERE course_id IN (SELECT course_id FROM course_lessons WHERE lesson_id=?)",
        (lesson_id,),
    )


# ---------- challenges ----------

def all_challenges():
    return _rows("SELECT * FROM challenges ORDER BY id")


def get_challenge(slug: str):
    return _one("SELECT * FROM challenges WHERE slug=?", (slug,))


def challenge_stats(challenge_id: int):
    return _one(
        "SELECT COUNT(*) AS attempts, "
        "SUM(CASE WHEN result='passed' THEN 1 ELSE 0 END) AS passed, "
        "COALESCE(SUM(hints_used),0) AS hints "
        "FROM challenge_attempts WHERE challenge_id=?",
        (challenge_id,),
    )


def passed_challenges_count() -> int:
    row = _one(
        "SELECT COUNT(DISTINCT challenge_id) AS c FROM challenge_attempts "
        "WHERE result='passed'"
    )
    return row["c"]


def add_attempt(challenge_id, attempt_number, result, execution_time, hints_used, code):
    _exec(
        "INSERT INTO challenge_attempts(challenge_id, attempt_number, result, "
        "execution_time, hints_used, submitted_at, code) "
        "VALUES(?,?,?,?,?,datetime('now'),?)",
        (challenge_id, attempt_number, result, execution_time, hints_used, code),
    )


# ---------- learning sessions (streak) ----------

def touch_session(date: str, minutes: int = 20):
    _exec(
        "INSERT INTO learning_sessions(date, minutes) VALUES(?,?)",
        (date, minutes),
    )


def learning_minutes() -> int:
    row = _one("SELECT COALESCE(SUM(minutes),0) AS m FROM learning_sessions")
    return row["m"]


def distinct_dates():
    return [r["date"] for r in _rows("SELECT DISTINCT date FROM learning_sessions")]


# ---------- interview prep ----------

def interview_progress_all() -> dict:
    rows = _rows("SELECT * FROM interview_progress")
    return {r["question_id"]: r for r in rows}


def interview_progress(question_id: str):
    return _one("SELECT * FROM interview_progress WHERE question_id=?", (question_id,))


def set_interview_status(question_id: str, status: str, choice: str | None = None):
    _exec(
        "INSERT INTO interview_progress(question_id,status,attempts,last_choice,updated_at) "
        "VALUES(?,?,1,?,datetime('now')) "
        "ON CONFLICT(question_id) DO UPDATE SET "
        "status=excluded.status, "
        "attempts=interview_progress.attempts + 1, "
        "last_choice=COALESCE(excluded.last_choice, interview_progress.last_choice), "
        "updated_at=excluded.updated_at",
        (question_id, status, choice),
    )


def reset_interview_status(question_id: str):
    _exec("DELETE FROM interview_progress WHERE question_id=?", (question_id,))


# ---------- notes / mistakes ----------

def list_notes():
    return _rows("SELECT * FROM notes ORDER BY id DESC")


def add_note(title, body, kind):
    return _exec(
        "INSERT INTO notes(title, body, kind, created_at) VALUES(?,?,?,datetime('now'))",
        (title, body, kind),
    )


def del_note(note_id):
    _exec("DELETE FROM notes WHERE id=?", (note_id,))


def list_mistakes():
    return _rows("SELECT * FROM mistakes ORDER BY id DESC")


def add_mistake(problem, cause, lesson, prevention):
    return _exec(
        "INSERT INTO mistakes(problem, cause, lesson, prevention, created_at) "
        "VALUES(?,?,?,?,datetime('now'))",
        (problem, cause, lesson, prevention),
    )


def del_mistake(mistake_id):
    _exec("DELETE FROM mistakes WHERE id=?", (mistake_id,))


# ---------- projects ----------

def get_projects():
    return _rows("SELECT * FROM projects ORDER BY id")


def project_stages(project_id):
    return _rows("SELECT * FROM project_tasks WHERE project_id=? ORDER BY id", (project_id,))
