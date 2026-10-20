from fastapi import APIRouter, Depends

from app.api.deps import current_user
from app.services import db

router = APIRouter()

PHASE_TITLES = {
    "python": "Python", "php": "PHP", "sql": "SQL", "codeigniter": "CodeIgniter",
    "laravel": "Laravel", "javascript": "JavaScript", "se": "Software Engineering",
    "interview": "Interview Prep",
}


@router.get("/api/progress")
def progress(user: dict = Depends(current_user)):
    lessons = db.get_lessons()
    done = db.completed_lesson_ids(user["id"])
    per_phase = {}
    for l in lessons:
        per_phase.setdefault(l["phase_slug"], {"total": 0, "done": 0})
        per_phase[l["phase_slug"]]["total"] += 1
        if l["id"] in done:
            per_phase[l["phase_slug"]]["done"] += 1

    rows = []
    for slug, counts in per_phase.items():
        pct = round(counts["done"] / counts["total"] * 100) if counts["total"] else 0
        rows.append({
            "phase": PHASE_TITLES.get(slug, slug),
            "pct": pct,
            "done": counts["done"],
            "total": counts["total"],
        })
    rows.sort(key=lambda r: -r["pct"])

    total = len(lessons)
    overall = round(len(done) / total * 100) if total else 0
    courses = [
        {
            "slug": row["slug"],
            "title": row["title"],
            "category": row["category"],
            "pct": round((row["lessons_completed"] or 0) / row["lessons_total"] * 100)
            if row["lessons_total"] else 0,
            "done": row["lessons_completed"] or 0,
            "total": row["lessons_total"] or 0,
            "enrolled": bool(row["enrolled"]),
        }
        for row in db.all_courses(user["id"])
    ]
    return {"overall": overall, "phases": rows, "courses": courses}
