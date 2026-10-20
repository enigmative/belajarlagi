from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.api.deps import current_user
from app.services import runner

router = APIRouter()


class RunRequest(BaseModel):
    code: str
    language: str = "python"


@router.post("/api/playground/run")
def run(req: RunRequest, user: dict = Depends(current_user)):
    if req.language != "python":
        return {"status": "error", "error": "language not supported yet"}
    res = runner.run_python(req.code)
    return res
