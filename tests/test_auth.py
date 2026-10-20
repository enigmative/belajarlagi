"""Authentication, public catalogue, and per-user isolation tests."""
import uuid
from datetime import datetime, timedelta, timezone

from app.services import auth, db

PASSWORD = "test-password-123"


def _create_user(prefix="auth", active=True):
    email = f"{prefix}-{uuid.uuid4().hex}@example.com"
    user_id = db.create_user(email, f"User {prefix}", auth.hash_password(PASSWORD))
    if not active:
        db.set_user_active(user_id, False)
    return user_id, email


def test_anonymous_catalogue_is_public_but_personal_pages_are_not(anon_client):
    courses = anon_client.get("/api/courses")
    assert courses.status_code == 200
    assert courses.json()["total"] == 19
    python_course = next(c for c in courses.json()["courses"] if c["slug"] == "python-fundamentals")
    assert python_course["enrolled"] is False
    assert python_course["lessons_completed"] == 0

    detail = anon_client.get("/api/courses/python-fundamentals")
    assert detail.status_code == 200
    assert detail.json()["modules"][0]["lessons"][0]["slug"] == "day01"
    assert detail.json()["enrolled"] is False

    assert anon_client.get("/api/lessons/day01").status_code == 401
    assert anon_client.get("/api/lessons").status_code == 401
    assert anon_client.get("/api/dashboard").status_code == 401
    assert anon_client.get("/api/my-learning").status_code == 401
    assert anon_client.get("/api/progress").status_code == 401
    assert anon_client.get("/api/roadmap").status_code == 401
    assert anon_client.get("/api/challenges").status_code == 401
    assert anon_client.get("/api/interview").status_code == 401
    assert anon_client.get("/api/notes").status_code == 401
    assert anon_client.get("/api/projects").status_code == 401
    assert anon_client.get("/api/search?q=python").status_code == 401
    assert anon_client.post(
        "/api/playground/run", json={"code": "print(1)", "language": "python"}
    ).status_code == 401


def test_login_me_logout(anon_client):
    _user_id, email = _create_user("login")

    bad = anon_client.post("/api/auth/login", json={"email": email, "password": "salah-password"})
    assert bad.status_code == 401

    missing = anon_client.post(
        "/api/auth/login", json={"email": "tidak-ada@example.com", "password": PASSWORD}
    )
    assert missing.status_code == 401

    login = anon_client.post("/api/auth/login", json={"email": email, "password": PASSWORD})
    assert login.status_code == 200
    assert login.json()["user"]["email"] == email
    assert "bl_session" in login.headers["set-cookie"]
    cookie = login.headers["set-cookie"].lower()
    assert "httponly" in cookie
    assert "samesite=lax" in cookie

    me = anon_client.get("/api/auth/me")
    assert me.status_code == 200
    assert me.json()["user"]["email"] == email

    assert anon_client.post("/api/auth/logout").status_code == 200
    assert anon_client.get("/api/auth/me").status_code == 401


def test_secure_cookie_when_https_is_enabled(anon_client, monkeypatch):
    _user_id, email = _create_user("secure")
    monkeypatch.setenv("BELAJAR_LAGI_HTTPS", "1")
    response = anon_client.post(
        "/api/auth/login", json={"email": email, "password": PASSWORD}
    )
    assert response.status_code == 200
    cookie = response.headers["set-cookie"].lower()
    assert "secure" in cookie


def test_inactive_user_cannot_login(anon_client):
    _user_id, email = _create_user("inactive", active=False)
    response = anon_client.post(
        "/api/auth/login", json={"email": email, "password": PASSWORD}
    )
    assert response.status_code == 401


def test_no_public_registration_endpoint(anon_client):
    response = anon_client.post(
        "/api/auth/register",
        json={"email": "baru@example.com", "password": PASSWORD},
    )
    assert response.status_code in (404, 405)


def test_password_reset_revokes_sessions(anon_client):
    user_id, email = _create_user("reset")
    assert anon_client.post(
        "/api/auth/login", json={"email": email, "password": PASSWORD}
    ).status_code == 200
    assert anon_client.get("/api/auth/me").status_code == 200

    new_password = "new-password-456"
    db.set_user_password(user_id, auth.hash_password(new_password))
    db.delete_user_sessions(user_id)
    assert anon_client.get("/api/auth/me").status_code == 401
    assert anon_client.post(
        "/api/auth/login", json={"email": email, "password": PASSWORD}
    ).status_code == 401
    assert anon_client.post(
        "/api/auth/login", json={"email": email, "password": new_password}
    ).status_code == 200


def test_expired_session_is_rejected(anon_client):
    user_id, email = _create_user("expiry")
    assert anon_client.post(
        "/api/auth/login", json={"email": email, "password": PASSWORD}
    ).status_code == 200

    past = (datetime.now(timezone.utc) - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    conn = db.get_conn()
    try:
        conn.execute(
            "UPDATE auth_sessions SET expires_at=? WHERE user_id=?", (past, user_id)
        )
        conn.commit()
    finally:
        conn.close()

    assert anon_client.get("/api/auth/me").status_code == 401


def test_two_users_have_separate_progress_notes_and_interview(client, client2):
    assert client.post("/api/lessons/day01/complete").status_code == 200
    assert client.post("/api/notes", json={"title": "catatan A", "body": "isi", "kind": "concept"}).status_code == 200
    assert client.post(
        "/api/interview/questions/core-06-static-autowired/answer", json={"choice": "a"}
    ).status_code == 200

    assert client.get("/api/dashboard").json()["lessons_completed"] == 1
    assert client2.get("/api/dashboard").json()["lessons_completed"] == 0
    assert client2.get("/api/my-learning").json()["courses"] == []
    assert client2.get("/api/notes").json() == []
    assert client2.get("/api/interview/questions/core-06-static-autowired").json()["status"] == "unseen"

    assert client2.post("/api/lessons/day02/complete").status_code == 200
    assert client.get("/api/dashboard").json()["lessons_completed"] == 1
    assert client2.get("/api/dashboard").json()["lessons_completed"] == 1

    courses = client.get("/api/courses").json()["courses"]
    python = next(c for c in courses if c["slug"] == "python-fundamentals")
    assert python["lessons_completed"] == 1

    courses2 = client2.get("/api/courses").json()["courses"]
    python2 = next(c for c in courses2 if c["slug"] == "python-fundamentals")
    assert python2["lessons_completed"] == 1
    assert client2.get("/api/courses/python-fundamentals").json()["lessons_completed"] == 1


def test_project_task_completion_is_per_user(client, client2):
    projects = client.get("/api/projects").json()
    project = projects[0]
    task = project["stages"][0]

    assert client.post(
        f"/api/projects/{project['slug']}/tasks/{task['id']}",
        json={"is_done": True},
    ).status_code == 200

    mine = client.get("/api/projects").json()[0]
    other = client2.get("/api/projects").json()[0]
    assert next(s for s in mine["stages"] if s["id"] == task["id"])["is_done"] == 1
    assert next(s for s in other["stages"] if s["id"] == task["id"])["is_done"] == 0


def test_course_enrollment_is_per_user(client, client2):
    assert client.post("/api/courses/sql-for-developers/enroll").status_code == 200
    assert client.get("/api/my-learning").json()["courses"]
    assert client2.get("/api/my-learning").json()["courses"] == []
