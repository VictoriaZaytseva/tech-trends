from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RepoBase(BaseModel):
    name: str
    url: str
    stars: int
    language: Optional[str]
    description: Optional[str]

class Repo(RepoBase):
    id: int
    fetched_at: datetime

    class Config:
        orm_mode = True