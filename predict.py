import asyncio
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import json
import tensorflow as tf
from market_price_movement_prediction.scrape_finance_data_yahoo import scrape_and_save_data
from multi_time_series_connectedness import (
    Volatility,
    RollingConnectedness,
)

# predict timestamp
max_lag = 20
past_roll_conn_period = 5
periods_per_volatility = 80
predict_timestamp = "2024-10-18T07:06:00+01:00"
train_tickers = ["AUDCAD=X", "AUDCHF=X", "AUDJPY=X", "AUDNZD=X", "CADCHF=X", "CADJPY=X", "CHFJPY=X"]
predict_ticker = "AUDCAD=X"
predict_data_dir = "docs/market_prices/predict"
volatilities_from = str((datetime.fromisoformat(predict_timestamp) - timedelta(minutes=past_roll_conn_period+periods_per_volatility+1)).isoformat())
volatilities_to = str(datetime.fromisoformat(predict_timestamp).isoformat())
train_from = str((datetime.fromisoformat(predict_timestamp) - timedelta(minutes=past_roll_conn_period)).isoformat())
train_to = str(datetime.fromisoformat(predict_timestamp).isoformat())
volatilities_filename = "docs/predict/volatilities.pickle"
roll_conn_filename = "docs/predict/roll_conn.pickle"

# Scrape data
print("scraping finance data for predicting")
asyncio.run(scrape_and_save_data(train_tickers, predict_data_dir))

print("calculating volatilities")
volatility = Volatility(n=2)
volatility.calculate(
    predict_data_dir,
    volatilities_from,
    volatilities_to,
    volatilities_filename,
)

print("calculate rolling connectedness")
volatilities = pd.read_pickle(volatilities_filename)
roll_conn = RollingConnectedness(
    volatilities.dropna(),
    max_lag,
    periods_per_volatility,
    train_from,
    train_to,
)
roll_conn.calculate(roll_conn_filename)

print("predict movements")
with open("docs/trained_model_metadata.json", "r") as f:
    metadata = json.load(f)
    model = tf.keras.models.load_model(metadata["model_path"])
with open(roll_conn_filename, "rb") as f:
    predict_roll_conn = pd.read_pickle(f)
columns_to_remove = ["start_at", "end_at", "forecast_at_next_period", "forecast_at"]
input_data = predict_roll_conn.drop(columns=columns_to_remove).values
input_data = np.expand_dims(input_data, axis=0)
predictions = model.predict(input_data)
print(predictions)
