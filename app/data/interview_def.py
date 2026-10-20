"""Metadata dan bank soal Interview Prep 3 hari.

Pola ini mirip `challenges_def.py`: konten soal dan jawaban tinggal di
backend, frontend hanya menerima data yang memang boleh ditampilkan.
"""

from app.data.interview_day1 import QUESTIONS_DAY1
from app.data.interview_day2 import QUESTIONS_DAY2
from app.data.interview_day3 import QUESTIONS_DAY3

INTERVIEW_DAYS = [
    {
        "day": 1,
        "title": "Hari 1 — Java & Membaca Kode",
        "lesson": "interview-day1",
        "goal": "Variable, tipe data, if, loop, method, class/object, interface, trace kode, dan NullPointerException.",
    },
    {
        "day": 2,
        "title": "Hari 2 — Spring Boot & JavaScript",
        "lesson": "interview-day2",
        "goal": "Bean, dependency injection, ApplicationContext, REST, JavaScript modern, GraphQL, dan Quarkus.",
    },
    {
        "day": 3,
        "title": "Hari 3 — React, Live Coding & Interview",
        "lesson": "interview-day3",
        "goal": "JSX, props, state, hooks, Context, live coding, dan latihan menjelaskan dengan suara keras.",
    },
]

INTERVIEW_QUESTIONS = QUESTIONS_DAY1 + QUESTIONS_DAY2 + QUESTIONS_DAY3


def _opt(*texts):
    return [{"id": chr(97 + i), "text": t} for i, t in enumerate(texts)]


# Opsi dan kunci MCQ dipusatkan di sini agar tidak ada kunci jawaban
# yang bocor ke frontend sebelum user menjawab.
_MCQ_DATA = {
    "core-02-react-import": (_opt(
        "import React.Component from 'react';",
        "import [ Component ] from 'react';",
        "import Component from 'react';",
        "import { Component } from 'react';",
    ), "d"),
    "core-03-react-hooks": (_opt(
        "Optimasi aplikasi mobile",
        "Membuat efek visual otomatis",
        "Memungkinkan state dan lifecycle di function component",
        "Mengintegrasikan library UI seperti Bootstrap",
    ), "c"),
    "core-04-react-context": (_opt(
        "React context",
        "Redux",
        "React Router",
        "React lifecycle methods",
    ), "a"),
    "core-06-static-autowired": (_opt(
        "formatter.getClass()",
        "context.containsBean(\"formatter\")",
        "context.getBean(\"formatter\").getClass()",
        "context.getClass()",
    ), "a"),
    "core-07-array-destructuring": (_opt(
        "Horse",
        "Cat",
        "Mouse",
        "Undefined",
    ), "b"),
    "react-01-props": (_opt(
        "Hello, Ada dan Hello, Guest",
        "Hello, Ada dan Hello,",
        "Hello, Guest dan Hello, Guest",
        "Error pada <Hello />",
    ), "a"),
    "react-02-usestate": (_opt(
        "0",
        "1",
        "2",
        "Error",
    ), "b"),
    "react-03-useeffect": (_opt(
        "Setiap kali komponen render",
        "Hanya setelah render pertama",
        "Sebelum komponen dirender",
        "Hanya saat komponen di-unmount",
    ), "b"),
    "react-04-context": (_opt(
        "light",
        "dark",
        "undefined",
        "Error karena Toolbar tidak menerima props",
    ), "b"),
    "react-05-import-export": (_opt(
        "5 6",
        "6 5",
        "5 5",
        "SyntaxError",
    ), "a"),
    "js-01-object-destructuring": (_opt(
        "Ada undefined",
        "Ada 20",
        "name 20",
        "undefined 20",
    ), "b"),
    "js-02-array-rest": (_opt(
        "10 30 [40, 50]",
        "10 20 [30, 40, 50]",
        "10 30 40",
        "10 undefined [40, 50]",
    ), "a"),
    "js-03-scope": (_opt(
        "1 2",
        "1 ReferenceError",
        "undefined 2",
        "ReferenceError ReferenceError",
    ), "b"),
    "js-04-hoisting": (_opt(
        "undefined lalu undefined",
        "ReferenceError lalu ReferenceError",
        "undefined lalu ReferenceError",
        "5 lalu 10",
    ), "c"),
    "js-05-map-filter": (_opt(
        "[10, 20, 30, 40, 50]",
        "[20, 40]",
        "[2, 4]",
        "[1, 3, 5]",
    ), "b"),
    "js-06-undefined-null": (_opt(
        "true false true \"object\"",
        "true true true \"null\"",
        "false false false \"object\"",
        "true false false \"null\"",
    ), "a"),
}

for _q in INTERVIEW_QUESTIONS:
    if _q["kind"] == "mcq":
        _options, _correct = _MCQ_DATA[_q["id"]]
        _q["options"] = _options
        _q["correct"] = _correct

QUESTION_BY_ID = {q["id"]: q for q in INTERVIEW_QUESTIONS}

if len(QUESTION_BY_ID) != len(INTERVIEW_QUESTIONS):
    raise ValueError("ID soal interview duplikat")

for _q in INTERVIEW_QUESTIONS:
    for _field in ("id", "day", "topic", "title", "kind", "origin", "points",
                   "concept", "prompt", "hints", "answer", "traps", "speak"):
        if _field not in _q:
            raise ValueError(f"Soal {_q.get('id')} tidak punya field {_field}")
    if len(_q["hints"]) != 2:
        raise ValueError(f"Soal {_q['id']} harus punya tepat 2 hint")
    if _q["kind"] == "mcq":
        if "options" not in _q or "correct" not in _q:
            raise ValueError(f"MCQ {_q['id']} tidak punya options/correct")
        if _q["correct"] not in {o["id"] for o in _q["options"]}:
            raise ValueError(f"MCQ {_q['id']} punya correct yang tidak valid")


def get_question(question_id: str) -> dict | None:
    return QUESTION_BY_ID.get(question_id)


def public_question(question: dict, progress: dict | None = None) -> dict:
    """Data untuk daftar soal: tanpa jawaban dan tanpa kunci MCQ."""
    out = {
        "id": question["id"],
        "day": question["day"],
        "topic": question["topic"],
        "title": question["title"],
        "kind": question["kind"],
        "origin": question["origin"],
        "points": question["points"],
        "status": (progress or {}).get("status", "unseen"),
        "attempts": (progress or {}).get("attempts", 0),
    }
    if question["kind"] == "mcq":
        out["options"] = [{"id": o["id"], "text": o["text"]} for o in question["options"]]
    return out
