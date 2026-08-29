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
    lessons = db.get_lessons()
    idx = next((i for i, l in enumerate(lessons) if l["slug"] == slug), None)
    prev = lessons[idx - 1] if idx and idx > 0 else None
    nxt = lessons[idx + 1] if idx is not None and idx + 1 < len(lessons) else None
    prog = db.get_progress(lesson["id"])
    return {
        **lesson,
        "markdown": md,
        "prev": {"slug": prev["slug"], "title": prev["title"]} if prev else None,
        "next": {"slug": nxt["slug"], "title": nxt["title"]} if nxt else None,
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
