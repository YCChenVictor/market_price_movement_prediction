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
        return {"message": "Market data scraped and saved successfully."}
    except Exception as e:
        print(e)
