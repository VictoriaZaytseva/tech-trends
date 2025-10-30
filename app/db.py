from sqlalchemy import ForeignKey, create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os
from app import settings

DATABASE_URL = settings.database_url
#os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/postgres")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Repo(Base):
    __tablename__ = "repos"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    language = Column(String, index=True)
    stars = Column(Integer)
    forks = Column(Integer)
    html_url = Column(String)
    fetched_at = Column(DateTime)

    stats = relationship("RepoStats", back_populates="repos")

class RepoStats(Base):
    __tablename__ = "repo_stats"

    id = Column(Integer, primary_key=True, index=True)
    repo_id = Column(Integer, ForeignKey("repos.id"))
    stars = Column(Integer)
    forks = Column(Integer)
    open_issues = Column(Integer)
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())

    repository = relationship("Repository", back_populates="stats")

def init_db():
    Base.metadata.create_all(bind=engine)