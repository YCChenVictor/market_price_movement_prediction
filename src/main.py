import logging
from fastapi import FastAPI
from src.api import app as api_app
from src.scheduler import start_scheduler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(api_app.router)


@app.on_event("startup")
def startup_event():
    start_scheduler()
