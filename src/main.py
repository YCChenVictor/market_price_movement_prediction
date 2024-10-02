import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import logging
from fastapi import FastAPI
from api import app as api_app
from scheduler import start_scheduler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(api_app.router)

@app.on_event("startup")
def startup_event():
    start_scheduler()
