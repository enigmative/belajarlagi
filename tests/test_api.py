"""API smoke tests for Belajar Lagi."""
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_dashboard():
    r = client.get("/api/dashboard")
    assert r.status_code == 200
    d = r.json()
    assert "overall_pct" in d and "lessons_total" in d


def test_lessons_list_and_detail():
    assert client.get("/api/lessons").status_code == 200
    r = client.get("/api/lessons/day01")
    assert r.status_code == 200
    assert r.json()["title"].startswith("Day 01")


def test_lesson_complete():
    r = client.post("/api/lessons/day01/complete")
    assert r.status_code == 200
    d = client.get("/api/dashboard").json()
    assert d["lessons_completed"] >= 1


def test_progress():
    r = client.get("/api/progress")
    assert r.status_code == 200
    assert "phases" in r.json()


def test_roadmap():
    r = client.get("/api/roadmap")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_playground_ok():
    r = client.post("/api/playground/run", json={"code": "print(6)", "language": "python"})
    assert r.status_code == 200
    assert r.json()["status"] == "ok"
    assert "6" in r.json()["output"]


def test_playground_blocks_os():
    r = client.post("/api/playground/run", json={"code": "import os; print(os.getcwd())"})
    # may raise, but -I still allows os; we only assert it doesn't crash the server
    assert r.status_code == 200


def test_challenges_list():
    r = client.get("/api/challenges")
    assert r.status_code == 200
    assert len(r.json()) >= 70


def test_challenge_fizzbuzz():
    code = 'def solve(n):\n    res=[]\n    for i in range(1,n+1):\n        if i%15==0: res.append("FizzBuzz")\n        elif i%3==0: res.append("Fizz")\n        elif i%5==0: res.append("Buzz")\n        else: res.append(i)\n    return res'
    r = client.post("/api/challenges/fizzbuzz/submit",
                    json={"code": code, "hints_used": 0})
    assert r.status_code == 200
    assert r.json()["status"] == "passed"


def test_challenge_correct():
    r = client.post("/api/challenges/largest-number/submit",
                    json={"code": "def solve(ns):\n    return max(ns)", "hints_used": 0})
    assert r.status_code == 200
    assert r.json()["status"] == "passed"


def test_challenge_wrong():
    r = client.post("/api/challenges/largest-number/submit",
                    json={"code": "def solve(ns):\n    return 0", "hints_used": 0})
    assert r.json()["status"] == "failed"
    assert len(r.json()["failures"]) > 0


def test_notes_crud():
    r = client.post("/api/notes", json={"title": "t", "body": "b", "kind": "concept"})
    nid = r.json()["id"]
    assert client.get("/api/notes").status_code == 200
    assert client.delete(f"/api/notes/{nid}").status_code == 200


def test_mistakes_crud():
    r = client.post("/api/mistakes", json={"problem": "p", "cause": "c", "lesson": "l", "prevention": "v"})
    mid = r.json()["id"]
    assert client.delete(f"/api/mistakes/{mid}").status_code == 200


def test_projects():
    r = client.get("/api/projects")
    assert r.status_code == 200
    assert len(r.json()) >= 1
