import logging
from fastapi import FastAPI
from .api import app as api_app
from .scheduler import start_scheduler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Include API routes
app.include_router(api_app.router)

@app.on_event("startup")
def startup_event():
    start_scheduler()
