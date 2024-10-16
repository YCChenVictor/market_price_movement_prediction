from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from influxdb_client import Point, WritePrecision

from src.db import write_api, INFLUXDB_BUCKET, INFLUXDB_ORG
from src.scrape_finance_data_yahoo import scrape_and_save_data


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
        point = (
            Point("volatility_data")
            .tag("symbol", data.symbol)
            .field("volatility", data.volatility)
            .time(data.timestamp, WritePrecision.NS)
        )

        write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)
        return {"message": "Volatility data written successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# maybe this one should be POST, but now we do not have database
@app.get("/get/market_data/")
async def scrape_market_data(symbols: list[str] = Query(...), directory: str = Query(...)):
    try:
        scrape_and_save_data(symbols, directory=directory)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
