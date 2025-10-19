from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
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

def init_db():
    Base.metadata.create_all(bind=engine)