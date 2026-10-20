"""Login/logout endpoints. Accounts are created by an admin via CLI."""
import os

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from pydantic import BaseModel

from app.api.deps import current_user
from app.services import auth, db

router = APIRouter()


class LoginBody(BaseModel):
    email: str
    password: str


def _public_user(user: dict) -> dict:
    return {
        "id": user["id"],
        "email": user["email"],
        "name": user["name"],
        "role": user["role"],
    }


def _secure_cookie(request: Request) -> bool:
    return (
        os.environ.get("BELAJAR_LAGI_HTTPS") == "1"
        or request.url.scheme == "https"
    )


@router.post("/api/auth/login")
def login(body: LoginBody, request: Request, response: Response):
    email = body.email.strip()
    user = db.get_user_by_email(email)
    if (
        not user
        or not user["is_active"]
        or not auth.verify_password(body.password, user["password_hash"])
    ):
        raise HTTPException(status_code=401, detail="Email atau password salah")

    token = auth.new_session_token()
    db.create_auth_session(
        user["id"],
        auth.hash_session_token(token),
        days=auth.SESSION_DAYS,
    )
    db.mark_user_login(user["id"])
    response.set_cookie(
        key=auth.SESSION_COOKIE,
        value=token,
        max_age=auth.SESSION_DAYS * 24 * 60 * 60,
        httponly=True,
        samesite="lax",
        secure=_secure_cookie(request),
        path="/",
    )
    return {"user": _public_user(user)}


@router.get("/api/auth/me")
def me(user: dict = Depends(current_user)):
    return {"user": _public_user(user)}


@router.post("/api/auth/logout")
def logout(request: Request, response: Response):
    token = request.cookies.get(auth.SESSION_COOKIE)
    if token:
        db.delete_auth_session(auth.hash_session_token(token))
    response.delete_cookie(
        key=auth.SESSION_COOKIE,
        path="/",
        httponly=True,
        samesite="lax",
        secure=_secure_cookie(request),
    )
    return {"ok": True}
