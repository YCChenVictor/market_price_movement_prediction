import logging
import time
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

logger = logging.getLogger(__name__)

def my_scheduled_job():
    logger.info(f"Job executed at {time.strftime('%Y-%m-%d %H:%M:%S')}")

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(my_scheduled_job, IntervalTrigger(seconds=10))
    scheduler.start()
