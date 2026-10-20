from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import current_user, optional_user
from app.services import db

router = APIRouter()


def _course_summary(row: dict) -> dict:
    total = row.get("lessons_total") or 0
    done = row.get("lessons_completed") or 0
    return {
        "slug": row["slug"],
        "title": row["title"],
        "description": row.get("description"),
        "category": row.get("category"),
        "level": row.get("level"),
        "icon": row.get("icon"),
        "order_index": row.get("order_index"),
        "lessons_total": total,
        "lessons_completed": done,
        "progress_pct": round(done / total * 100) if total else 0,
        "enrolled": bool(row.get("enrolled")),
    }


def _course_payload(row: dict, user_id: int = 0) -> dict:
    course = _course_summary(row)
    modules = []
    lessons = db.course_lessons(user_id, row["id"])
    by_module = {}
    for lesson in lessons:
        by_module.setdefault(lesson["module_id"], []).append({
            "slug": lesson["slug"],
            "title": lesson["title"],
            "completed": bool(lesson["completed"]),
            "order_index": lesson["course_order"],
        })

    for module in db.course_modules(row["id"]):
        module_lessons = by_module.get(module["id"], [])
        if not module_lessons:
            continue
        modules.append({
            "slug": module["slug"],
            "title": module["title"],
            "description": module.get("description"),
            "order_index": module["order_index"],
            "lessons": module_lessons,
        })

    next_lesson = next((l for l in lessons if not l["completed"]), lessons[-1] if lessons else None)
    course["modules"] = modules
    course["next_lesson"] = (
        {"slug": next_lesson["slug"], "title": next_lesson["title"]}
        if next_lesson else None
    )
    return course


@router.get("/api/courses")
def list_courses(user: dict | None = Depends(optional_user)):
    user_id = user["id"] if user else 0
    rows = db.all_courses(user_id)
    courses = [_course_summary(row) for row in rows]
    categories = sorted({c["category"] for c in courses if c["category"]})
    return {"courses": courses, "total": len(courses), "categories": categories}


@router.get("/api/courses/{slug}")
def get_course(slug: str, user: dict | None = Depends(optional_user)):
    user_id = user["id"] if user else 0
    row = db.get_course(user_id, slug)
    if not row:
        raise HTTPException(404, "course not found")
    return _course_payload(row, user_id)


@router.post("/api/courses/{slug}/enroll")
def enroll_course(slug: str, user: dict = Depends(current_user)):
    row = db.get_course(user["id"], slug)
    if not row:
        raise HTTPException(404, "course not found")
    db.enroll_course(user["id"], row["id"])
    row = db.get_course(user["id"], slug)
    payload = _course_payload(row, user["id"])
    return {
        "ok": True,
        "course": payload["slug"],
        "next_lesson": payload["next_lesson"],
    }


@router.get("/api/my-learning")
def my_learning(user: dict = Depends(current_user)):
    rows = db.all_courses(user["id"], enrolled_only=True)
    return {
        "courses": [_course_summary(row) for row in rows],
        "total": len(rows),
    }
