import os
import logging
import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from influxdb_client import InfluxDBClient, Point, WritePrecision
from pathlib import Path
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)
INFLUXDB_URL = os.getenv("INFLUXDB_URL")
INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN")
INFLUXDB_ORG = os.getenv("INFLUXDB_ORG")
INFLUXDB_BUCKET = os.getenv("INFLUXDB_BUCKET")

client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
write_api = client.write_api()

app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VolatilityData(BaseModel):
    symbol: str
    volatility: float
    timestamp: str

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.post("/write/volatility/")
async def write_data(data: VolatilityData):
    try:
        point = Point("volatility_data") \
            .tag("symbol", data.symbol) \
            .field("volatility", data.volatility) \
            .time(data.timestamp, WritePrecision.NS)

        write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)
        return {"message": "Volatility data written successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def my_scheduled_job():
    logger.info(f"Job executed at {time.strftime('%Y-%m-%d %H:%M:%S')}")

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(my_scheduled_job, IntervalTrigger(seconds=10))
    scheduler.start()

@app.on_event("startup")
def startup_event():
    start_scheduler()
