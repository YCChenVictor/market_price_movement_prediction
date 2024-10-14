# Process:
# scrape finance data from yahoo finance
# modify data to deal with NAN and repeat data problem
# calculate volatility
# calculate movements
# calculate rolling connectedness
# add rolling connectedness (used only when there is new connectedness)
# Turn data into TFRecord format
# train model (CNN, RNN, ConvLSTM)
# predict movement (CNN, RNN, ConvLSTM)

import pandas as pd
from scrape_finance_data_yahoo import scrape_and_save_data
from etl import ETL
from multi_time_series_connectedness import (
    Volatility,
    Connectedness,
    RollingConnectedness,
)
from movement import Movement
from model_trainer import ModelTrainer
import argparse
import sys


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Script with array and other variables"
    )
    parser.add_argument(
        "--train_features_tickers",
        nargs="+",
        type=str,
        help="Array of tickers to train the model",
    )
    parser.add_argument("--train_data_dir", type=str, help="Directory to save the data")
    parser.add_argument(
        "--train_predict_ticker", type=str, help="Ticker to predict the movement"
    )
    args = parser.parse_args()
    train_tickers = args.train_features_tickers
    train_data_dir = args.train_data_dir
    train_predict_ticker = args.train_predict_ticker
    print(f"Features Array: {train_tickers}")

    print("scraping finance data")
    scrape_and_save_data(train_tickers, train_data_dir)

    print("modifying data")
    etl = ETL(train_data_dir)
    etl.process()

    print("calculating volatilities")
    volatility = Volatility(n=2)
    volatility.calculate(
        "docs/market_prices/train",
        "2024-10-11 00:00:00+01:00",
        "2024-10-11 22:29:00+01:00",
        "docs/volatilities.pickle",
    )

    print("calculate rolling connectedness")
    volatilities = pd.read_pickle("docs/volatilities.pickle")
    print(volatilities)
    max_lag = 20
    periods_per_volatility = 80
    roll_conn = RollingConnectedness(
        volatilities.dropna(),
        max_lag,
        periods_per_volatility,
        "2024-10-11 01:21:00+01:00",
        "2024-10-11 22:00:00+01:00",
    )
    roll_conn.calculate("docs/train/roll_conn.pickle")

    print("calculate movements")
    movement = Movement(
        f"docs/market_prices/train/{train_predict_ticker}.csv", "docs/movement.pickle"
    )
    movement.get_movements("value")
    movement.store()

    print("train LSTM model")
    with open("docs/train/movement.pickle", "rb") as f:
        movement = pd.read_pickle(f)
    with open("docs/train/roll_conn.pickle", "rb") as f:
        roll_conn = pd.read_pickle(f)
    model_trainer = ModelTrainer(movement, roll_conn, 5, train_tickers)
    model_trainer.match()
    model_trainer.train()

    # print("predict movements")
    # data_to_predict -> It will be the same format of the connectedness, so actually, there some be two threads on parallel, one keeps training the model, one keeps predicting the movements
    # predictions = model_trainer.predict(data_to_predict)
