from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

from app.api.routes import (
    auth, dashboard, lessons, progress, playground, challenges, notes, search, projects,
    interview, courses,
)
from database.database import init_db

ROOT = os.path.dirname(os.path.dirname(__file__))
FRONTEND = os.path.join(ROOT, "frontend")

app = FastAPI(title="Belajar Lagi")

init_db()

app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(lessons.router)
app.include_router(progress.router)
app.include_router(playground.router)
app.include_router(challenges.router)
app.include_router(notes.router)
app.include_router(search.router)
app.include_router(projects.router)
app.include_router(interview.router)
app.include_router(courses.router)

app.mount("/static", StaticFiles(directory=os.path.join(FRONTEND, "css")), name="css")
app.mount("/js", StaticFiles(directory=os.path.join(FRONTEND, "js")), name="js")


@app.get("/")
def index():
    return FileResponse(os.path.join(FRONTEND, "index.html"))


@app.get("/{path:path}")
def spa(path: str):
    # ponytail: any unknown path serves index.html; SPA routes client-side
    if path == "api" or path.startswith("api/"):
        raise HTTPException(status_code=404)
    root = os.path.realpath(FRONTEND)
    candidate = os.path.realpath(os.path.join(root, path))
    try:
        inside = os.path.commonpath([root, candidate]) == root
    except ValueError:
        inside = False
    if inside and os.path.isfile(candidate):
        return FileResponse(candidate)
    return FileResponse(os.path.join(root, "index.html"))
