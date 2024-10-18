import json
import tensorflow as tf
import numpy as np
import argparse
from scrape_finance_data_yahoo import scrape_and_save_data
from multi_time_series_connectedness import RollingConnectedness
import pandas as pd


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script with other variables")
    parser.add_argument(
        "--predict_ticker", type=str, help="Ticker to predict the movement"
    )
    parser.add_argument(
        "--timestamp", type=str, help="Timestamp to predict the movement"
    )
    args = parser.parse_args()
    predict_ticker = args.predict_ticker
    timestamp = args.timestamp

    volatilities = pd.read_pickle("docs/volatilities.pickle")
    max_lag = 20
    periods_per_volatility = 80
    roll_conn = RollingConnectedness(
        volatilities.dropna(),
        max_lag,
        periods_per_volatility,
        "2024-10-11 22:22:00+01:00",
        "2024-10-11 22:29:00+01:00",
    )
    roll_conn.calculate("docs/predict/roll_conn.pickle")

    with open("docs/trained_model_metadata.json", "r") as f:
        metadata = json.load(f)
    model = tf.keras.models.load_model(metadata["model_path"])
    scrape_and_save_data(metadata["feature_tickers"], "docs/market_prices/predict")

    print("predict movements")
    with open("docs/predict/roll_conn.pickle", "rb") as f:
        predict_roll_conn = pd.read_pickle(f)
    columns_to_remove = ["start_at", "end_at", "forecast_at_next_period", "forecast_at"]
    input_data = predict_roll_conn.drop(columns=columns_to_remove).values
    input_data = np.expand_dims(input_data, axis=0)
    predictions = model.predict(input_data)
    print(predictions)
