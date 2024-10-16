from unittest.mock import patch
from fastapi.testclient import TestClient
from src.routers.data import market_data_router # I think this is wrong
import pandas as pd

client = TestClient(market_data_router)


def mock_get_historical_price(symbol):
    if symbol == 'AAPL':
        return [
            {'time': '2024-10-16T15:01:00+01:00', 'symbol':  'AAPL', 'Open': 0.918749988079071, 'High': 0.918749988079071, 'Low': 0.918749988079071, 'Close': 0.918749988079071}
        ]
    elif symbol == 'GOOG':
        return [
            {'time': '2024-10-16T00:00:00+01:00', 'symbol': 'GOOG', 'Open': 0.5775200128555298, 'High': 0.5776200294494629, 'Low': 0.5774999856948853, 'Close': 0.5776000022888184}
        ]
    else:
        return None


@patch("src.scrape_finance_data_yahoo.get_historical_price_with_yfinace")
def test_scrape_market_data(mock_get_historical_price_with_yfinace):
    mock_get_historical_price_with_yfinace.side_effect = mock_get_historical_price

    response = client.post("/market_data/", params={"symbols": ["AAPL", "GOOG"], "directory": "docs/market_prices/train"})

    assert response.status_code == 200
    assert response.json() == {"message": "Market data scraped and saved successfully."}


@patch("os.listdir")
@patch("pandas.read_csv")
def test_list_market_data_info(mock_read_csv, mock_listdir):
    mock_listdir.return_value = ['AAPL.csv', 'GOOG.csv']

    mock_df_aapl = pd.DataFrame([{'time': '2024-10-16T15:01:00+01:00', 'symbol':  'AAPL', 'Open': 0.918749988079071, 'High': 0.918749988079071, 'Low': 0.918749988079071, 'Close': 0.918749988079071}, {'time': '2024-10-16T15:02:00+01:00', 'symbol':  'AAPL', 'Open': 0.918749988079071, 'High': 0.918749988079071, 'Low': 0.918749988079071, 'Close': 0.918749988079071}])
    mock_df_goog = pd.DataFrame([{'time': '2024-10-16T00:00:00+01:00', 'symbol': 'GOOG', 'Open': 0.5775200128555298, 'High': 0.5776200294494629, 'Low': 0.5774999856948853, 'Close': 0.5776000022888184}, {'time': '2024-10-16T00:01:00+01:00', 'symbol': 'GOOG', 'Open': 0.5775200128555298, 'High': 0.5776200294494629, 'Low': 0.5774999856948853, 'Close': 0.5776000022888184}])

    def mock_read_csv_side_effect(filepath, *args, **kwargs):
        if 'AAPL.csv' in filepath:
            return mock_df_aapl
        elif 'GOOG.csv' in filepath:
            return mock_df_goog
        else:
            return pd.DataFrame()

    mock_read_csv.side_effect = mock_read_csv_side_effect

    response = client.get("/market_data/", params={"directory": "docs/market_prices/train"})

    assert response.status_code == 200
    assert response.json() == {
        'AAPL.csv': ['2024-10-16T15:01:00+01:00', '2024-10-16T15:02:00+01:00'],
        'GOOG.csv': ['2024-10-16T00:00:00+01:00', '2024-10-16T00:01:00+01:00']
    }
