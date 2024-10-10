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
from load_and_modify_data import load_and_process_market_data
from multi_time_series_connectedness import Volatility, Connectedness, RollingConnectedness
from movement import Movement
from model_trainer import ModelTrainer

# # Turn data into TFRecord format
# print("turning data format into TFRecord")
# import flows.data_TFRecord_format as data_TFRecord_format

# # train model CNN (還在 version1)
# """
# print("training model CNN")
# import train_model_CNN
# """

# # train model RNN
# """
# 這邊要設計一個依照上次checkpoint後繼續training的選項
# print("training model RNN")
# import train_model_RNN
# """

# # train model CNN_RNN (ConvLSTM) (還在 version1)
# """
# print("training model CNN + RNN")
# import train_model_CNN_RNN
# """

# # make prediction CNN

# # make prediction RNN
# print("make prediction")
# import flows.predict_RNN as predict_RNN

# # make prediction ConvLSTM


# # count the elapsed time span, end time
# elapsed_time = time.time() - start_time
# print("the time span in all procedure: ", elapsed_time)
# print("===================")


if __name__ == "__main__":
    symbols = [
        # "AAPL",
        # "AMZN",
        "AUDCAD=X",
        "AUDCHF=X",
        "AUDJPY=X",
        "AUDNZD=X",
        # "AUDUSD=X",
        # "^AXJO",
        "CADCHF=X",
        "CADJPY=X",
        "CHFJPY=X",
        # "DX-Y.NYB",
        "EURAUD=X",
        "EURCAD=X",
        "EURCHF=X",
        "EURGBP=X",
        "EURJPY=X",
        "EURNZD=X",
        # "EURUSD=X",
        # "^STOXX50E",
        "GBPAUD=X",
        "GBPCAD=X",
        "GBPCHF=X",
        "GBPJPY=X",
        "GBPNZD=X",
        # "GBPUSD=X",
        # "^GDAXI",
        # "GOOGL",
        # "^N225",
        # "MSFT",
        # "NQ=F",
        "NZDCAD=X",
        "NZDCHF=X",
        "NZDJPY=X",
        # "NZDUSD=X",
        # "^SPX",
        # "TSLA",
        # "^FTSE",
        "USDCAD=X",
        "USDCHF=X",
        "USDJPY=X",
        # "USO",
        # "SI=F",
        # "GC=F",
    ]
    # print("scraping finance data")
    # scrape_and_save_data(symbols)
    # print("modifying data")
    # load_and_process_market_data("docs/market_prices/")
    # print("calculating volatilities")
    # volatility = Volatility(n=2)
    # volatility.calculate("2024-10-09T00:00:00+01:00", "2024-10-09T09:59:00+01:00", "docs/market_prices", "docs/volatilities.pickle")

    # print("calculate full connectedness")
    # volatilities = pd.read_pickle("docs/volatilities.pickle")
    # print(volatilities)
    # connectedness = Connectedness(volatilities)
    # connectedness.calculate()

    # print("calculate rolling connectedness")
    # roll_conn = RollingConnectedness(volatilities.dropna(), 20, 80)
    # roll_conn.divide_timeseries_volatilities()
    # roll_conn.calculate("docs/roll_conn.pickle")

    # print("calculate movements")
    # movement = Movement("docs/market_prices/AUDCAD=X.csv", "docs/movement.pickle")
    # movement.get_movements("value")
    # movement.store()

    # print("train LSTM model")
    with open("docs/movement.pickle", "rb") as f:
        movement = pd.read_pickle(f)
    with open("docs/roll_conn.pickle", "rb") as f:
        roll_conn = pd.read_pickle(f)
    model_trainer = ModelTrainer(movement, roll_conn)
    model_trainer.match(5)
    # model_trainer.train()

    # print("predict movements")
