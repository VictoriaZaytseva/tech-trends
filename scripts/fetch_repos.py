import requests
import datetime
from sqlalchemy.orm import Session
from app.db import SessionLocal, Repo, init_db
from app.errors import logger
from sqlalchemy.exc import SQLAlchemyError
from requests.exceptions import RequestException

def fetch_trending():
    url = "https://api.github.com/search/repositories"
    params = {
        "q": "created:>2025-01-01",
        "sort": "stars",
        "order": "desc",
        "per_page": 20
    }
    r = requests.get(url, params=params)
    r.raise_for_status()
    return r.json()["items"]

def save_to_db(items):
    db: Session = SessionLocal()
    for item in items:
        print(f"Saving repo: {item['full_name']} with {item['stargazers_count']} stars")
        repo = Repo(
            id=item["id"],
            name=item["full_name"],
            language=item["language"],
            stars=item["stargazers_count"],
            forks=item["forks_count"],
            html_url=item["html_url"],
            fetched_at=datetime.datetime.utcnow()
        )
        db.merge(repo)
    db.commit()
    db.close()

if __name__ == "__main__":
    try:
        init_db()
        items = fetch_trending()
        save_to_db(items)
        logger.info("Fetched and saved trending repos.")
    except RequestException as e:
        logger.error(f"GitHub API error: {e}")
    except SQLAlchemyError as e:
        logger.error(f"Database error: {e}")
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")