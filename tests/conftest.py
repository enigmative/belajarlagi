"""Pytest setup: every test run gets its own SQLite database.

The app reads BELAJAR_LAGI_DB when database.database is imported, so this
must run before any test module imports app.main or database.database.
"""
import os
import shutil
import tempfile
from pathlib import Path

import pytest

_TEST_DIR = Path(tempfile.mkdtemp(prefix="belajar_lagi_test_"))
_TEST_DB = _TEST_DIR / "learning.db"
os.environ["BELAJAR_LAGI_DB"] = str(_TEST_DB)


@pytest.fixture(scope="session", autouse=True)
def _seeded_test_database():
    from database.database import init_db
    from scripts.seed import seed

    init_db()
    seed()
    yield
    shutil.rmtree(_TEST_DIR, ignore_errors=True)
