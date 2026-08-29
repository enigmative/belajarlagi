from fastapi import APIRouter
from pydantic import BaseModel

from app.services import content, db

router = APIRouter()


@router.get("/api/search")
def search(q: str = ""):
    q = q.lower()
    items = content.search_index()
    if not q:
        return []
    out = []
    for it in items:
        if q in it["text"].lower() or q in it["title"].lower():
            out.append({"slug": it["slug"], "title": it["slug"], "folder": it["folder"]})
    return out[:20]
