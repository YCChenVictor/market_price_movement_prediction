from unittest.mock import patch, mock_open
from fastapi.testclient import TestClient
from src.api import app

client = TestClient(app)


def mock_get_historical_price(symbol):
    if symbol == 'AAPL':
        return [{'time': '2024-10-16T15:01:00+01:00', 'symbol':  'AAPL', 'Open': 0.918749988079071, 'High': 0.918749988079071, 'Low': 0.918749988079071, 'Close': 0.918749988079071}]
    elif symbol == 'GOOG':
        return [{'time': '2024-10-16T00:00:00+01:00', 'symbol': 'GOOG', 'Open': 0.5775200128555298, 'High': 0.5776200294494629, 'Low': 0.5774999856948853, 'Close': 0.5776000022888184}]
    else:
        return None


@patch("src.scrape_finance_data_yahoo.get_historical_price_with_yfinace")
def test_scrape_market_data(mock_get_historical_price_with_yfinace):
    mock_get_historical_price_with_yfinace.side_effect = mock_get_historical_price
    
    response = client.get("/get/market_data/", params={"symbols": ["AAPL", "GOOG"], "directory": "docs/market_prices/train"})
    
    assert response.status_code == 200
    assert response.json() == {"message": "Market data scraped and saved successfully."}
