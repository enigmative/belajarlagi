from datetime import date, timedelta

from fastapi import APIRouter

from app.services import db
from app.services import content

router = APIRouter()

# priority weight per phase name used in `/progress` display
PHASE_TITLES = {
    "python": "Python", "php": "PHP", "sql": "SQL", "codeigniter": "CodeIgniter",
    "laravel": "Laravel", "javascript": "JavaScript", "se": "Software Engineering",
    "interview": "Interview Prep",
}


def _streak(dates: set) -> int:
    # ponytail: streak = consecutive days ending today (or yesterday if no session today yet)
    dates = {d for d in dates}
    streak = 0
    cursor = date.today()
    for _ in range(400):
        if cursor.isoformat() in dates:
            streak += 1
            cursor -= timedelta(days=1)
            continue
        if streak == 0:
            cursor -= timedelta(days=1)
            continue
        break
    return streak


@router.get("/api/dashboard")
def dashboard():
    lessons = db.get_lessons()
    total = len(lessons) or 1
    completed = db.completed_lessons()

    # current lesson = first not-completed in order
    current = None
    done_ids = db.completed_lesson_ids()
    for l in lessons:
        if l["id"] not in done_ids:
            current = l
            break
    if current is None and lessons:
        current = lessons[-1]

    minutes = db.learning_minutes()
    dates = db.distinct_dates()

    challenges = db.all_challenges()
    ch_attempts = sum(db.challenge_stats(c["id"])["attempts"] or 0 for c in challenges)
    ch_passed = sum(db.challenge_stats(c["id"])["passed"] or 0 for c in challenges)

    return {
        "overall_pct": round(completed / total * 100),
        "current_phase": current["phase_slug"] if current else None,
        "current_lesson": {"slug": current["slug"], "title": current["title"]} if current else None,
        "streak": _streak(set(dates)),
        "lessons_completed": completed,
        "lessons_total": total,
        "challenges_passed": ch_passed,
        "challenges_total": len(challenges),
        "challenge_attempts": ch_attempts,
        "learning_minutes": minutes,
        "learning_time": _fmt_time(minutes),
    }


def _fmt_time(minutes: int) -> str:
    h, m = divmod(minutes, 60)
    return f"{h}h {m}m"
