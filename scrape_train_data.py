import asyncio
from market_price_movement_prediction.scrape_finance_data_yahoo import scrape_and_save_data
from market_price_movement_prediction.etl import ETL

# Define arguments
tickers = ['AUDCAD=X', 'AUDCHF=X', 'AUDJPY=X', 'AUDNZD=X', 'CADCHF=X', 'CADJPY=X', 'CHFJPY=X']
train_data_dir = 'docs/market_prices/train'
volatilities_from = "2024-10-18 00:00:00+01:00"
volatilities_to = "2024-10-18 06:00:00+01:00"
volatilities_filename = "docs/volatilities_train.pickle"

# scrape data from training
print("scraping finance data for training")
asyncio.run(scrape_and_save_data(tickers, train_data_dir))

# Process the data
print("modifying data")
etl = ETL(train_data_dir)
etl.process()
etl.check_same_time_span()
