"""Tests for the course catalogue and course-aware lesson navigation."""


def test_course_catalogue_has_all_courses(client):
    r = client.get("/api/courses")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 19
    assert "Python Fundamentals" in [c["title"] for c in data["courses"]]
    assert "Interview Prep" in [c["title"] for c in data["courses"]]
    assert "Programming" in data["categories"]


def test_course_detail_groups_lessons_into_modules(client):
    r = client.get("/api/courses/python-fundamentals")
    assert r.status_code == 200
    course = r.json()
    assert course["slug"] == "python-fundamentals"
    assert course["lessons_total"] == 9
    assert len(course["modules"]) == 2
    assert course["modules"][0]["lessons"][0]["slug"] == "day01"
    slugs = {l["slug"] for m in course["modules"] for l in m["lessons"]}
    assert course["next_lesson"]["slug"] in slugs


def test_lesson_uses_course_navigation(client):
    lesson = client.get("/api/lessons/day02").json()
    assert lesson["course"]["slug"] == "python-fundamentals"
    assert lesson["prev"]["slug"] == "day01"
    assert lesson["next"]["slug"] == "day03"


def test_enroll_and_my_learning(client):
    r = client.post("/api/courses/sql-for-developers/enroll")
    assert r.status_code == 200
    assert r.json()["course"] == "sql-for-developers"

    my = client.get("/api/my-learning").json()
    assert any(c["slug"] == "sql-for-developers" for c in my["courses"])

    detail = client.get("/api/courses/sql-for-developers").json()
    assert detail["enrolled"] is True


def test_finishing_a_lesson_adds_course_to_my_learning(client):
    assert client.post("/api/lessons/day01/complete").status_code == 200
    my = client.get("/api/my-learning").json()
    course = next(c for c in my["courses"] if c["slug"] == "python-fundamentals")
    assert course["enrolled"] is True
    assert course["lessons_total"] == 9
    assert course["lessons_completed"] >= 1


def test_dashboard_points_at_current_course(client):
    dashboard = client.get("/api/dashboard").json()
    assert dashboard["current_course"]["slug"] == "python-fundamentals"
    assert dashboard["current_lesson"]["course_slug"] == "python-fundamentals"


def test_unknown_course_returns_404(client):
    assert client.get("/api/courses/tidak-ada").status_code == 404
    assert client.post("/api/courses/tidak-ada/enroll").status_code == 404
