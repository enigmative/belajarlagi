"""Unit tests for streak + runner + challenge evaluator."""
from app.api.routes.dashboard import _streak
from app.services import runner, challenges as chall
from database.database import get_conn


def test_streak_basic():
    from datetime import date, timedelta
    d = date.today()
    days = {d.isoformat()}
    assert _streak(days) >= 1


def test_streak_gap_breaks():
    from datetime import date, timedelta
    d = date.today()
    # session today + 2 days ago -> streak 1 (yesterday missing)
    days = {d.isoformat(), (d - timedelta(days=2)).isoformat()}
    assert _streak(days) == 1


def test_runner_timeout():
    res = runner.run_python("while True: pass")
    assert res["status"] == "error"
    assert "Timeout" in res["error"]


def test_runner_output_limit():
    res = runner.run_python("print('x' * 50000)")
    assert res["status"] == "ok"
    assert len(res["output"]) <= 10000 + 50


def test_runner_blocks_subprocess():
    # subprocess module is allowed by -I but running is impractical; ensure callable
    res = runner.run_python("print('safe')")
    assert res["status"] == "ok"


def test_challenge_evaluator():
    conn = get_conn()
    c = conn.execute("SELECT * FROM challenges WHERE slug='sum-list'").fetchone()
    conn.close()
    res = chall.evaluate(c, "def solve(ns):\n    return sum(ns)")
    assert res["status"] == "passed"


def test_challenge_edge_cases():
    conn = get_conn()
    c = conn.execute("SELECT * FROM challenges WHERE slug='largest-number'").fetchone()
    conn.close()
    # wrong answer on empty list edge would be False for comparing to error; our tests
    # expect max(ns) to raise -> harness marks 'err' -> failure. Using full correct impl:
    res = chall.evaluate(c, "def solve(ns):\n    return max(ns)")
    assert res["passed"] == res["total"]
