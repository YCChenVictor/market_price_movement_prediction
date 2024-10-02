from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from influxdb_client import Point, WritePrecision
from db import write_api, INFLUXDB_BUCKET, INFLUXDB_ORG

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
