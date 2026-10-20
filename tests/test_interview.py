"""Tests for the Interview Prep question bank and progress API."""


def _reset(client, question_id: str):
    client.post(f"/api/interview/questions/{question_id}/reset")


def test_interview_list_has_three_days_and_49_questions(client):
    r = client.get("/api/interview")
    assert r.status_code == 200
    data = r.json()
    assert len(data["days"]) == 3
    assert data["overall"]["total"] == 49
    assert len(data["questions"]) == 49
    assert {d["day"] for d in data["days"]} == {1, 2, 3}
    assert all(d["total"] > 0 for d in data["days"])
    assert all(len(d["topics"]) >= 1 for d in data["days"])


def test_interview_every_question_has_analogy_and_two_hints():
    from app.data.interview_def import INTERVIEW_QUESTIONS

    assert len(INTERVIEW_QUESTIONS) == 49
    for q in INTERVIEW_QUESTIONS:
        assert "Analogi" in q["concept"], q["id"]
        assert len(q["hints"]) == 2, q["id"]
        assert q["traps"], q["id"]
        assert q["speak"].strip(), q["id"]


def test_interview_question_detail_never_leaks_mcq_key_before_answer(client):
    _reset(client, "core-06-static-autowired")
    r = client.get("/api/interview/questions/core-06-static-autowired")
    assert r.status_code == 200
    q = r.json()
    assert "correct" not in q
    assert "correct_choice" not in q
    assert len(q["options"]) == 4
    assert q["status"] == "unseen"
    assert "answer" in q and "hints" in q and len(q["hints"]) == 2


def test_interview_mcq_answer_wrong_then_correct_and_reset(client):
    qid = "core-06-static-autowired"
    _reset(client, qid)

    r = client.post(f"/api/interview/questions/{qid}/answer", json={"choice": "b"})
    assert r.status_code == 200
    assert r.json()["correct"] is False
    assert r.json()["status"] == "wrong"
    assert r.json()["correct_choice"] == "a"

    detail = client.get(f"/api/interview/questions/{qid}").json()
    assert detail["status"] == "wrong"
    assert detail["last_choice"] == "b"
    assert detail["correct_choice"] == "a"

    r = client.post(f"/api/interview/questions/{qid}/answer", json={"choice": "a"})
    assert r.status_code == 200
    assert r.json()["correct"] is True
    assert r.json()["status"] == "correct"

    _reset(client, qid)
    assert client.get(f"/api/interview/questions/{qid}").json()["status"] == "unseen"


def test_interview_mcq_rejects_invalid_choice(client):
    _reset(client, "core-06-static-autowired")
    r = client.post("/api/interview/questions/core-06-static-autowired/answer", json={"choice": "z"})
    assert r.status_code == 400


def test_interview_mcq_status_cannot_bypass_answer_validation(client):
    qid = "core-06-static-autowired"
    _reset(client, qid)
    r = client.post(f"/api/interview/questions/{qid}/status", json={"status": "correct"})
    assert r.status_code == 400
    assert client.get(f"/api/interview/questions/{qid}").json()["status"] == "unseen"


def test_interview_open_question_self_assessment(client):
    qid = "core-01-unknown-sequence"
    _reset(client, qid)
    r = client.post(f"/api/interview/questions/{qid}/status", json={"status": "correct"})
    assert r.status_code == 200
    assert r.json()["status"] == "correct"
    assert client.get(f"/api/interview/questions/{qid}").json()["status"] == "correct"

    r = client.post(f"/api/interview/questions/{qid}/status", json={"status": "wrong"})
    assert r.status_code == 200
    assert client.get(f"/api/interview/questions/{qid}").json()["status"] == "wrong"

    _reset(client, qid)
    assert client.get(f"/api/interview/questions/{qid}").json()["status"] == "unseen"


def test_interview_open_question_rejects_mcq_answer_endpoint(client):
    _reset(client, "core-01-unknown-sequence")
    r = client.post("/api/interview/questions/core-01-unknown-sequence/answer", json={"choice": "a"})
    assert r.status_code == 400


def test_interview_unknown_question_returns_404(client):
    assert client.get("/api/interview/questions/tidak-ada").status_code == 404
    assert client.post("/api/interview/questions/tidak-ada/reset").status_code == 404


def test_interview_summary_reflects_status(client):
    qid = "core-06-static-autowired"
    _reset(client, qid)
    before = client.get("/api/interview/summary").json()["overall"]
    client.post(f"/api/interview/questions/{qid}/answer", json={"choice": "a"})
    after = client.get("/api/interview/summary").json()["overall"]
    assert after["correct"] == before["correct"] + 1
    assert after["total"] == 49
    _reset(client, qid)


def test_interview_lessons_and_roadmap_are_registered(client):
    for slug in ("interview-day1", "interview-day2", "interview-day3"):
        r = client.get(f"/api/lessons/{slug}")
        assert r.status_code == 200
        assert len(r.json()["markdown"]) > 1000

    roadmap = client.get("/api/roadmap").json()
    assert any(group["phase"] == "interview" for group in roadmap)
