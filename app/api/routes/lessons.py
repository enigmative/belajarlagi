from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services import db, content

router = APIRouter()


@router.get("/api/lessons")
def list_lessons():
    return db.get_lessons()


@router.get("/api/lessons/{slug}")
def get_lesson(slug: str):
    lesson = db.get_lesson(slug)
    if not lesson:
        raise HTTPException(404, "lesson not found")
    md = content.load_markdown(slug)
    if md is None:
        md = "# (belum ada konten) " + slug

    course = db.course_for_lesson(lesson["id"])
    course_lessons = db.course_lessons(course["id"]) if course else []
    if course_lessons:
        idx = next((i for i, l in enumerate(course_lessons) if l["slug"] == slug), None)
        prev = course_lessons[idx - 1] if idx and idx > 0 else None
        nxt = course_lessons[idx + 1] if idx is not None and idx + 1 < len(course_lessons) else None
    else:
        lessons = db.get_lessons()
        idx = next((i for i, l in enumerate(lessons) if l["slug"] == slug), None)
        prev = lessons[idx - 1] if idx and idx > 0 else None
        nxt = lessons[idx + 1] if idx is not None and idx + 1 < len(lessons) else None

    course_payload = None
    if course:
        lessons_by_module = {}
        for item in course_lessons:
            lessons_by_module.setdefault(item["module_id"], []).append({
                "slug": item["slug"],
                "title": item["title"],
                "completed": bool(item["completed"]),
            })
        modules = []
        for module in db.course_modules(course["id"]):
            items = lessons_by_module.get(module["id"], [])
            if items:
                modules.append({
                    "slug": module["slug"],
                    "title": module["title"],
                    "lessons": items,
                })
        completed = sum(1 for item in course_lessons if item["completed"])
        course_payload = {
            **course,
            "modules": modules,
            "lessons_total": len(course_lessons),
            "lessons_completed": completed,
            "progress_pct": round(completed / len(course_lessons) * 100) if course_lessons else 0,
        }

    prog = db.get_progress(lesson["id"])
    return {
        **lesson,
        "markdown": md,
        "prev": {"slug": prev["slug"], "title": prev["title"]} if prev else None,
        "next": {"slug": nxt["slug"], "title": nxt["title"]} if nxt else None,
        "course": course_payload,
        "completed": bool(prog and prog["status"] == "completed"),
    }


class Complete(BaseModel):
    pass


@router.post("/api/lessons/{slug}/complete")
def complete_lesson(slug: str):
    lesson = db.get_lesson(slug)
    if not lesson:
        raise HTTPException(404, "lesson not found")
    db.mark_complete(lesson["id"])
    course = db.course_for_lesson(lesson["id"])
    if course:
        db.enroll_course(course["id"])
    db.touch_course_access_for_lesson(lesson["id"])
    db.touch_session(__import__("datetime").date.today().isoformat())
    return {"ok": True}


@router.get("/api/roadmap")
def roadmap():
    done = db.completed_lesson_ids()
    lessons = {l["slug"]: l for l in db.get_lessons()}
    tree = []
    for group in content.ROADMAP:
        topics = []
        for t in group["topics"]:
            slug = t["lesson"]
            state = "not_started"
            if slug and slug in done:
                state = "completed"
            elif slug:
                state = "current"
            topics.append({"title": t["title"], "lesson": slug, "status": state})
        tree.append({"name": group["name"], "phase": group["phase"], "topics": topics})
    return tree
