from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services import db

router = APIRouter()


class Note(BaseModel):
    title: str
    body: str
    kind: str = "concept"


@router.get("/api/notes")
def list_notes():
    return db.list_notes()


@router.post("/api/notes")
def create_note(n: Note):
    return {"id": db.add_note(n.title, n.body, n.kind)}


@router.delete("/api/notes/{note_id}")
def delete_note(note_id: int):
    db.del_note(note_id)
    return {"ok": True}


class Mistake(BaseModel):
    problem: str
    cause: str = ""
    lesson: str = ""
    prevention: str = ""


@router.get("/api/mistakes")
def list_mistakes():
    return db.list_mistakes()


@router.post("/api/mistakes")
def create_mistake(m: Mistake):
    return {"id": db.add_mistake(m.problem, m.cause, m.lesson, m.prevention)}


@router.delete("/api/mistakes/{mistake_id}")
def delete_mistake(mistake_id: int):
    db.del_mistake(mistake_id)
    return {"ok": True}
