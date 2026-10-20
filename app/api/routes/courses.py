from fastapi import APIRouter, HTTPException

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


def _course_payload(row: dict) -> dict:
    course = _course_summary(row)
    modules = []
    lessons = db.course_lessons(row["id"])
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
    course["enrolled"] = bool(course["enrolled"]) or bool(db.course_enrollment(row["id"]))
    return course


@router.get("/api/courses")
def list_courses():
    rows = db.all_courses()
    courses = [_course_summary(row) for row in rows]
    categories = sorted({c["category"] for c in courses if c["category"]})
    return {"courses": courses, "total": len(courses), "categories": categories}


@router.get("/api/courses/{slug}")
def get_course(slug: str):
    row = db.get_course(slug)
    if not row:
        raise HTTPException(404, "course not found")
    return _course_payload(row)


@router.post("/api/courses/{slug}/enroll")
def enroll_course(slug: str):
    row = db.get_course(slug)
    if not row:
        raise HTTPException(404, "course not found")
    db.enroll_course(row["id"])
    payload = _course_payload(row)
    return {
        "ok": True,
        "course": payload["slug"],
        "next_lesson": payload["next_lesson"],
    }


@router.get("/api/my-learning")
def my_learning():
    rows = db.all_courses(enrolled_only=True)
    return {
        "courses": [_course_summary(row) for row in rows],
        "total": len(rows),
    }
