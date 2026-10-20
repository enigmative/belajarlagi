from fastapi import APIRouter, Depends

from app.api.deps import current_user
from app.services import content

router = APIRouter()


@router.get("/api/search")
def search(q: str = "", user: dict = Depends(current_user)):
    q = q.lower()
    items = content.search_index()
    if not q:
        return []
    out = []
    for it in items:
        if q in it["text"].lower() or q in it["title"].lower():
            out.append({"slug": it["slug"], "title": it["slug"], "folder": it["folder"]})
    return out[:20]
