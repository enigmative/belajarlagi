"""FastAPI dependencies for the current account."""
from fastapi import HTTPException, Request

from app.services import auth, db


def optional_user(request: Request) -> dict | None:
    token = request.cookies.get(auth.SESSION_COOKIE)
    if not token:
        return None
    return db.user_for_session_token(auth.hash_session_token(token))


def current_user(request: Request) -> dict:
    user = optional_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="Silakan masuk terlebih dahulu")
    return user
