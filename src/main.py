from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from influxdb_client import InfluxDBClient, Point, WritePrecision
import os

INFLUXDB_URL = os.getenv("INFLUXDB_URL")
INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN")
INFLUXDB_ORG = os.getenv("INFLUXDB_ORG")
INFLUXDB_BUCKET = os.getenv("INFLUXDB_BUCKET")
client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
write_api = client.write_api()

app = FastAPI()

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
