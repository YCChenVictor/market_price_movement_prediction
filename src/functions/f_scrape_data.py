from time import sleep
from urllib.parse import urlparse
from urllib.parse import parse_qs
import sys
import yfinance as yf
import json
import pprint


def download_yahoo_quotes(ticker, period_seconds, driver):
    """
    :param ticker: the company
    :return: the web including specific csv file I want
    """
    driver.get(
        "https://query1.finance.yahoo.com/v7/finance/download/{0}"
        "?period1=0&period2={1}"
        "&interval=1d&events=history".format(ticker, period_seconds)
    )
    sleep(1)


def get_historical_price_with_yfinace(symbol):
    ticker = yf.Ticker(symbol)
    historical_prices = ticker.history(period="1d", interval="1m")
    historical_price_data = [
        {
            **{"time": index.isoformat(), "symbol": symbol},
            **row[["Open", "High", "Low", "Close"]].to_dict(),
        }
        for index, row in historical_prices.iterrows()
    ]
    return historical_price_data
