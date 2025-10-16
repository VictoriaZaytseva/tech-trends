from fastapi import FastAPI
from app import db
from app.api import router

app = FastAPI(title="Tech Trends Tracker")

@app.on_event("startup")
def startup():
    db.init_db()

app.include_router(router)

@app.get("/health")
def health():
    return {"status": "ok"}