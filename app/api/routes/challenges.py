from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.api.deps import current_user
from app.services import db
from app.services import challenges as chall

router = APIRouter()


def _public(c, user_id: int):
    return {
        "slug": c["slug"], "title": c["title"], "language": c["language"],
        "difficulty": c["difficulty"], "topic": c["topic"], "statement": c["statement"],
        "hint1": c["hint1"], "hint2": c["hint2"], "starter_code": c["starter_code"],
        "stats": db.challenge_stats(user_id, c["id"]),
    }


@router.get("/api/challenges")
def list_challenges(user: dict = Depends(current_user)):
    return [_public(c, user["id"]) for c in db.all_challenges()]


@router.get("/api/challenges/{slug}")
def get_challenge(slug: str, user: dict = Depends(current_user)):
    c = db.get_challenge(slug)
    if not c:
        raise HTTPException(404, "challenge not found")
    return _public(c, user["id"])


class Submit(BaseModel):
    code: str
    hints_used: int = 0


@router.post("/api/challenges/{slug}/submit")
def submit_challenge(slug: str, body: Submit, user: dict = Depends(current_user)):
    c = db.get_challenge(slug)
    if not c:
        raise HTTPException(404, "challenge not found")
    result = chall.evaluate(c, body.code, body.hints_used)
    stats = db.challenge_stats(user["id"], c["id"])
    attempt_number = (stats["attempts"] or 0) + 1
    db.add_attempt(
        user["id"], c["id"], attempt_number, result.get("status", "failed"),
        result.get("time", 0), body.hints_used, body.code,
    )
    if result.get("status") == "passed":
        db.touch_session(user["id"], __import__("datetime").date.today().isoformat())
    result["attempt_number"] = attempt_number
    return result
