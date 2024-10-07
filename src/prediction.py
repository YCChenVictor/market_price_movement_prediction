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

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import json
import os
import time
import functions.f_about_path as fap

# scrape finance data from yahoo finance
print("scraping finance data")
import flows.scrape_finance_data_yahoo as scrape_finance_data_yahoo

# modify data to deal with NAN and repeat data problem
print("modifying data")
import flows.load_and_modify_data as load_and_modify_data

# calculate volatilities
print("calculating volatilities")
import flows.calculate_volatility as calculate_volatility

# calculate movements (should have the option to select label or value)
print("calculating movements")
import flows.movement as movement

# calculate rolling connectedness
if prerequisite["iscontinue_conn"]:
    print("add new rolling connectedness")
    import flows.add_roll_conn as add_roll_conn
else:
    print("calculating rolling connectedness")
    import flows.roll_conn as roll_conn

# Turn data into TFRecord format (這部分應該要先放棄，因為官方也說不清楚怎麼用tfrecord訓練模型)
print("turning data format into TFRecord")
import flows.data_TFRecord_format as data_TFRecord_format

# train model CNN (還在 version1)
"""
print("training model CNN")
import train_model_CNN
"""

# train model RNN
"""
這邊要設計一個依照上次checkpoint後繼續training的選項
print("training model RNN")
import train_model_RNN
"""

# train model CNN_RNN (ConvLSTM) (還在 version1)
"""
print("training model CNN + RNN")
import train_model_CNN_RNN
"""

# make prediction CNN

# make prediction RNN
print("make prediction")
import flows.predict_RNN as predict_RNN

# make prediction ConvLSTM


# count the elapsed time span, end time
elapsed_time = time.time() - start_time
print("the time span in all procedure: ", elapsed_time)
print("===================")
