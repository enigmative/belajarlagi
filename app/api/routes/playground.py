from fastapi import APIRouter
from pydantic import BaseModel

from app.services import runner

router = APIRouter()


class RunRequest(BaseModel):
    code: str
    language: str = "python"


@router.post("/api/playground/run")
def run(req: RunRequest):
    if req.language != "python":
        return {"status": "error", "error": "language not supported yet"}
    res = runner.run_python(req.code)
    return res
