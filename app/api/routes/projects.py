from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.api.deps import current_user
from app.services import db

router = APIRouter()


@router.get("/api/projects")
def projects(user: dict = Depends(current_user)):
    out = []
    for p in db.get_projects():
        stages = db.project_stages(user["id"], p["id"])
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
def toggle_task(slug: str, task_id: int, body: TaskToggle, user: dict = Depends(current_user)):
    if not db.toggle_project_task(user["id"], slug, task_id, body.is_done):
        raise HTTPException(404, "task not found")
    return {"ok": True}
