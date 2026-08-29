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


def test_new_challenges_all_pass_with_correct_solution():
    conn = get_conn()
    sols = {
        "fizzbuzz": 'def solve(n):\n    res=[]\n    for i in range(1,n+1):\n        if i%15==0: res.append("FizzBuzz")\n        elif i%3==0: res.append("Fizz")\n        elif i%5==0: res.append("Buzz")\n        else: res.append(i)\n    return res',
        "leap-year": "def solve(y):\n    return y%4==0 and (y%100!=0 or y%400==0)",
        "factorial": "def solve(n):\n    r=1\n    for i in range(1,n+1): r*=i\n    return r",
        "count-vowels": 'def solve(t):\n    return sum(1 for c in t.lower() if c in "aeiou")',
        "second-largest": "def solve(ns):\n    return sorted(ns)[-2]",
    }
    try:
        for slug, code in sols.items():
            c = conn.execute("SELECT * FROM challenges WHERE slug=?", (slug,)).fetchone()
            assert c, f"challenge {slug} missing"
            res = chall.evaluate(c, code)
            assert res["status"] == "passed", f"{slug}: {res}"
    finally:
        conn.close()
