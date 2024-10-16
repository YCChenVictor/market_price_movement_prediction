import os
import pandas as pd
from fastapi import APIRouter, Query

from src.scrape_finance_data_yahoo import scrape_and_save_data
from src.etl import ETL

market_data_router = APIRouter()


# maybe this one should be POST, but now we do not have database
@market_data_router.post("/market_data/")
async def scrape_market_data(symbols: list[str] = Query(...), directory: str = Query(...)):
    try:
        await scrape_and_save_data(symbols, directory)
        etl = ETL(directory)
        etl.process()
        return {"message": "Market data scraped and saved successfully."}
    except Exception as e:
        print(e)


@market_data_router.get("/market_data/")
async def list_market_data_info(directory):
    try:
        dict = {}
        files = os.listdir(directory)
        csv_files = [file for file in files if file.endswith('.csv')]
        for csv_file in csv_files:
            data = pd.read_csv(os.path.join(directory, csv_file))
            dict[csv_file] = [data.iloc[0]['time'], data.iloc[-1]['time']]
        return dict
    except Exception as e:
        print(e)
