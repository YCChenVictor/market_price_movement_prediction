import logging
import yfinance as yf
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

logger = logging.getLogger(__name__)


def scrape_yfinance():
    ticker = yf.Ticker("AAPL")  # use this one now
    historical_prices = ticker.history(period="1d", interval="1m")
    historical_price_data = [
        {
            **{"time": index.isoformat(), "symbol": "AAPL"},
            **row[["Open", "High", "Low", "Close"]].to_dict(),
        }
        for index, row in historical_prices.iterrows()
    ]
    logger.info(historical_price_data)


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(scrape_yfinance, CronTrigger(second="5"))
    scheduler.start()
