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

@router.get("/archive")
def get_trending_from_archive(db: Session = Depends(get_db)):
    result = (
        db.query(
            Repository.full_name,
            func.count(RepoStats.id).label("star_events")
        )
        .join(RepoStats, Repository.id == RepoStats.repo_id)
        .filter(RepoStats.recorded_at >= datetime.utcnow() - timedelta(days=1))
        .group_by(Repository.full_name)
        .order_by(func.count(RepoStats.id).desc())
        .limit(10)
        .all()
    )
    return [{"repo": r.full_name, "stars": r.star_events} for r in result]