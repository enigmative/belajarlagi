from datetime import date
from typing import Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.data import interview_def as idef
from app.services import db

router = APIRouter()

VALID_STATUS = {"unseen", "wrong", "correct"}


def _progress_map() -> dict:
    return db.interview_progress_all()


def _day_summary(day: dict, questions: list[dict], progress: dict) -> dict:
    topics: dict[str, dict] = {}
    counts = {"total": 0, "correct": 0, "wrong": 0, "unseen": 0}

    for q in questions:
        status = (progress.get(q["id"]) or {}).get("status", "unseen")
        if status not in VALID_STATUS:
            status = "unseen"

        counts["total"] += 1
        counts[status] += 1

        topic = topics.setdefault(
            q["topic"], {"topic": q["topic"], "total": 0, "correct": 0, "wrong": 0, "unseen": 0}
        )
        topic["total"] += 1
        topic[status] += 1

    def pct(done: int, total: int) -> int:
        return round(done / total * 100) if total else 0

    for t in topics.values():
        t["pct"] = pct(t["correct"], t["total"])
        t["attempted"] = t["correct"] + t["wrong"]

    return {
        "day": day["day"],
        "title": day["title"],
        "lesson": day["lesson"],
        "goal": day["goal"],
        "total": counts["total"],
        "correct": counts["correct"],
        "wrong": counts["wrong"],
        "unseen": counts["unseen"],
        "attempted": counts["correct"] + counts["wrong"],
        "pct": pct(counts["correct"], counts["total"]),
        "topics": list(topics.values()),
    }


def _summary(progress: dict | None = None) -> dict:
    if progress is None:
        progress = _progress_map()
    questions_by_day = {d["day"]: [] for d in idef.INTERVIEW_DAYS}
    for q in idef.INTERVIEW_QUESTIONS:
        questions_by_day.setdefault(q["day"], []).append(q)

    days = [_day_summary(d, questions_by_day.get(d["day"], []), progress) for d in idef.INTERVIEW_DAYS]

    total = sum(d["total"] for d in days)
    correct = sum(d["correct"] for d in days)
    wrong = sum(d["wrong"] for d in days)
    unseen = sum(d["unseen"] for d in days)

    return {
        "days": days,
        "overall": {
            "total": total,
            "correct": correct,
            "wrong": wrong,
            "unseen": unseen,
            "attempted": correct + wrong,
            "pct": round(correct / total * 100) if total else 0,
        },
    }


def _touch_session_once_today():
    today = date.today().isoformat()
    if today not in db.distinct_dates():
        db.touch_session(today)


@router.get("/api/interview")
def list_interview():
    progress = _progress_map()
    data = _summary(progress)
    data["questions"] = [idef.public_question(q, progress.get(q["id"])) for q in idef.INTERVIEW_QUESTIONS]
    return data


@router.get("/api/interview/summary")
def interview_summary():
    return _summary()


@router.get("/api/interview/questions/{question_id}")
def get_interview_question(question_id: str):
    question = idef.get_question(question_id)
    if not question:
        raise HTTPException(404, "question not found")

    progress = db.interview_progress(question_id) or {}
    out = {k: v for k, v in question.items() if k != "correct"}
    out = dict(out)
    out["status"] = progress.get("status", "unseen")
    out["attempts"] = progress.get("attempts", 0)
    out["last_choice"] = progress.get("last_choice")
    if question["kind"] == "mcq" and out["status"] in ("wrong", "correct"):
        # Kunci hanya dibuka setelah user mencoba menjawab.
        out["correct_choice"] = question["correct"]
    return out


class AnswerBody(BaseModel):
    choice: str


class StatusBody(BaseModel):
    status: Literal["unseen", "wrong", "correct"]


@router.post("/api/interview/questions/{question_id}/answer")
def answer_interview_question(question_id: str, body: AnswerBody):
    question = idef.get_question(question_id)
    if not question:
        raise HTTPException(404, "question not found")
    if question["kind"] != "mcq":
        raise HTTPException(400, "question is not multiple choice")

    valid = {o["id"] for o in question["options"]}
    if body.choice not in valid:
        raise HTTPException(400, "invalid choice")

    correct = body.choice == question["correct"]
    status = "correct" if correct else "wrong"
    db.set_interview_status(question_id, status, body.choice)
    _touch_session_once_today()

    return {
        "correct": correct,
        "correct_choice": question["correct"],
        "status": status,
    }


@router.post("/api/interview/questions/{question_id}/status")
def set_interview_question_status(question_id: str, body: StatusBody):
    question = idef.get_question(question_id)
    if not question:
        raise HTTPException(404, "question not found")
    if question["kind"] == "mcq" and body.status != "unseen":
        raise HTTPException(400, "MCQ status is set through the answer endpoint")

    if body.status == "unseen":
        db.reset_interview_status(question_id)
    else:
        db.set_interview_status(question_id, body.status)
        _touch_session_once_today()

    return {"question_id": question_id, "status": body.status}


@router.post("/api/interview/questions/{question_id}/reset")
def reset_interview_question(question_id: str):
    question = idef.get_question(question_id)
    if not question:
        raise HTTPException(404, "question not found")
    db.reset_interview_status(question_id)
    return {"question_id": question_id, "status": "unseen"}
