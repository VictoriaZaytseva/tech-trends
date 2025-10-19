from fastapi import FastAPI
from app import db, errors, scheduler
from app.api import router
from sqlalchemy.exc import SQLAlchemyError
from requests.exceptions import RequestException

app = FastAPI(title="Tech Trends Tracker")

app.add_exception_handler(Exception, errors.global_exception_handler)
app.add_exception_handler(SQLAlchemyError, errors.db_exception_handler)
app.add_exception_handler(RequestException, errors.external_api_handler)

@app.on_event("startup")
def start_background_tasks():
    scheduler.start_scheduler()

@app.on_event("startup")
def startup():
    db.init_db()

app.include_router(router)

@app.get("/health")
def health():
    return {"status": "ok"}