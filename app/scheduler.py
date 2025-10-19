import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.errors import logger
from app.db import SessionLocal
from app.models import Repo
from scripts.fetch_repos import fetch_github_repos, save_to_db  # reuse your existing logic

def update_github_data():
    logger.info("⏳ Starting scheduled GitHub data fetch...")
    try:
        # Example: fetch trending Scala repos
        repos = fetch_github_repos(language="Scala")
        db = SessionLocal()
        save_to_db(db, repos)
        db.close()
        logger.info("✅ Successfully updated GitHub data.")
    except Exception as e:
        logger.exception(f"Scheduler job failed: {e}")

def start_scheduler():
    scheduler = BackgroundScheduler()
    # Run every 6 hours
    scheduler.add_job(update_github_data, IntervalTrigger(hours=6))
    scheduler.start()
    logger.info("🚀 APScheduler started (every 6 hours).")