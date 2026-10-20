from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.api.deps import current_user
from app.services import db

router = APIRouter()


class Note(BaseModel):
    title: str
    body: str
    kind: str = "concept"


@router.get("/api/notes")
def list_notes(user: dict = Depends(current_user)):
    return db.list_notes(user["id"])


@router.post("/api/notes")
def create_note(n: Note, user: dict = Depends(current_user)):
    return {"id": db.add_note(user["id"], n.title, n.body, n.kind)}


@router.delete("/api/notes/{note_id}")
def delete_note(note_id: int, user: dict = Depends(current_user)):
    db.del_note(user["id"], note_id)
    return {"ok": True}


class Mistake(BaseModel):
    problem: str
    cause: str = ""
    lesson: str = ""
    prevention: str = ""


@router.get("/api/mistakes")
def list_mistakes(user: dict = Depends(current_user)):
    return db.list_mistakes(user["id"])


@router.post("/api/mistakes")
def create_mistake(m: Mistake, user: dict = Depends(current_user)):
    return {"id": db.add_mistake(user["id"], m.problem, m.cause, m.lesson, m.prevention)}


@router.delete("/api/mistakes/{mistake_id}")
def delete_mistake(mistake_id: int, user: dict = Depends(current_user)):
    db.del_mistake(user["id"], mistake_id)
    return {"ok": True}
