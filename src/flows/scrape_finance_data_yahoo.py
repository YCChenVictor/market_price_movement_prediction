import yfinance as yf
import pandas as pd


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


def scrape_and_save_data(symbols):
    for symbol in symbols:
        result = get_historical_price_with_yfinace(symbol)
        pd.DataFrame(result).to_csv(f"./docs/market_prices/{symbol}.csv")
        print(result)
