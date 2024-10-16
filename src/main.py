import logging
from fastapi import FastAPI
from src.api import app as api_app
from src.routers.data import market_data_router
# from src.scheduler import start_scheduler


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(market_data_router)
