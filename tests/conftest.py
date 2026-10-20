"""Pytest setup: every test run gets its own SQLite database.

The app reads BELAJAR_LAGI_DB when database.database is imported, so this
must run before any test module imports app.main or database.database.
"""
import os
import shutil
import tempfile
import uuid
from pathlib import Path

import pytest

_TEST_DIR = Path(tempfile.mkdtemp(prefix="belajar_lagi_test_"))
_TEST_DB = _TEST_DIR / "learning.db"
os.environ["BELAJAR_LAGI_DB"] = str(_TEST_DB)

TEST_PASSWORD = "test-password-123"


@pytest.fixture(scope="session", autouse=True)
def _seeded_test_database():
    from database.database import init_db
    from scripts.seed import seed

    init_db()
    seed()
    yield
    shutil.rmtree(_TEST_DIR, ignore_errors=True)


def _make_user_client(prefix: str = "user"):
    from fastapi.testclient import TestClient

    from app.main import app
    from app.services import auth, db

    email = f"{prefix}-{uuid.uuid4().hex}@example.com"
    user_id = db.create_user(email, f"Test {prefix}", auth.hash_password(TEST_PASSWORD))
    client = TestClient(app)
    response = client.post(
        "/api/auth/login",
        json={"email": email, "password": TEST_PASSWORD},
    )
    assert response.status_code == 200, response.text
    client.user = response.json()["user"]
    client.user_id = user_id
    return client


@pytest.fixture
def client():
    test_client = _make_user_client("user")
    yield test_client
    test_client.close()


@pytest.fixture
def client2():
    test_client = _make_user_client("other")
    yield test_client
    test_client.close()


@pytest.fixture
def anon_client():
    from fastapi.testclient import TestClient

    from app.main import app

    test_client = TestClient(app)
    yield test_client
    test_client.close()
