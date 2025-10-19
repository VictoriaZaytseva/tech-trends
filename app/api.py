from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import SessionLocal, Repo

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/trending")
def trending_repos(db: Session = Depends(get_db)):
    repos = db.query(Repo).order_by(Repo.stars.desc()).limit(10).all()
    if not repos:
        raise HTTPException(status_code=404, detail=f"No repos found")
    return repos