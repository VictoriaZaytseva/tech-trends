import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    github_api_url: str = "https://api.github.com/search/repositories"
    token: str | None = None
    #TODO: configure db
    database_url: str
    # redis_url: str
    # scheduler_interval_hours: int
    # log_level: str

    class Config:
        env_file = os.getenv("ENV_FILE", ".env.local")
        env_file_encoding = "utf-8"