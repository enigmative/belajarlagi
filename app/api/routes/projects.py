from fastapi import APIRouter
from pydantic import BaseModel

from app.services import db

router = APIRouter()


@router.get("/api/projects")
def projects():
    out = []
    for p in db.get_projects():
        stages = db.project_stages(p["id"])
        done = sum(1 for s in stages if s["is_done"])
        out.append({
            "id": p["id"], "name": p["name"], "slug": p["slug"],
            "stages": [dict(s) for s in stages],
            "done": done, "total": len(stages),
        })
    return out


class TaskToggle(BaseModel):
    is_done: bool


@router.post("/api/projects/{slug}/tasks/{task_id}")
def toggle_task(slug: str, task_id: int, body: TaskToggle):
    db._exec("UPDATE project_tasks SET is_done=? WHERE id=?", (1 if body.is_done else 0, task_id))
    return {"ok": True}
