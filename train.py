import pandas as pd
from multi_time_series_connectedness import (
    Volatility,
    RollingConnectedness,
)
from market_price_movement_prediction.movement import Movement
from market_price_movement_prediction.model_trainer import ModelTrainer

market_prices_dir = "docs/market_prices/train"
train_tickers = ["AUDCAD=X", "AUDCHF=X", "AUDJPY=X", "AUDNZD=X", "CADCHF=X", "CADJPY=X", "CHFJPY=X"]
volatilities_filename = "docs/train/volatilities.pickle"
roll_conn_filename = "docs/train/roll_conn.pickle"
movement_filename = "docs/train/movement.pickle"
max_lag = 20
# train_from >= volatilities_from + periods_per_volatility
periods_per_volatility = 80
volatilities_from = "2024-10-18 00:00:00+01:00"
volatilities_to = "2024-10-18 06:00:00+01:00"
train_from = "2024-10-18 01:21:00+01:00"
train_to = "2024-10-18 06:00:00+01:00"
predict_ticker = "AUDCAD=X"
past_roll_conn_period = 5

print("calculating volatilities")
volatility = Volatility(n=2)
volatility.calculate(
    market_prices_dir,
    volatilities_from,
    volatilities_to,
    volatilities_filename,
)

# Should enable choosing the tickers
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

print("calculate movements")
movement = Movement(
    f"docs/market_prices/train/{predict_ticker}.csv", movement_filename
)
movement.get_movements("value")
movement.store()

print("train LSTM model")
with open(movement_filename, "rb") as f:
    movement = pd.read_pickle(f)
with open(roll_conn_filename, "rb") as f:
    roll_conn = pd.read_pickle(f)
model_trainer = ModelTrainer(movement, roll_conn, past_roll_conn_period, train_tickers)
model_trainer.match()
model_trainer.train()
