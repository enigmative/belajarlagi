from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

from app.api.routes import (
    dashboard, lessons, progress, playground, challenges, notes, search, projects, interview,
)
from database.database import init_db

ROOT = os.path.dirname(os.path.dirname(__file__))
FRONTEND = os.path.join(ROOT, "frontend")

app = FastAPI(title="Belajar Lagi")

init_db()

app.include_router(dashboard.router)
app.include_router(lessons.router)
app.include_router(progress.router)
app.include_router(playground.router)
app.include_router(challenges.router)
app.include_router(notes.router)
app.include_router(search.router)
app.include_router(projects.router)
app.include_router(interview.router)

app.mount("/static", StaticFiles(directory=os.path.join(FRONTEND, "css")), name="css")
app.mount("/js", StaticFiles(directory=os.path.join(FRONTEND, "js")), name="js")


@app.get("/")
def index():
    return FileResponse(os.path.join(FRONTEND, "index.html"))


@app.get("/{path:path}")
def spa(path: str):
    # ponytail: any unknown path serves index.html; SPA routes client-side
    candidate = os.path.join(FRONTEND, path)
    if os.path.exists(candidate) and not os.path.isdir(candidate):
        return FileResponse(candidate)
    return FileResponse(os.path.join(FRONTEND, "index.html"))
