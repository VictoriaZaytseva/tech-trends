from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Shared fields (used for both DB reads and API responses)
class RepoBase(BaseModel):
    name: str
    url: str
    stars: int
    language: Optional[str]
    description: Optional[str]

# This is what the API returns (includes ID + timestamps)
class Repo(RepoBase):
    id: int
    fetched_at: datetime

    class Config:
        orm_mode = True