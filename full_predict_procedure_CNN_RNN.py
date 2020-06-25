# conclusion:
# 1. CNN 不能用（training accuracy 無法上升）
# 2. LSTM 還可以用（training accuracy 可以上到 100%）
# 3. ConvLSTM

# problem:
# 1. 把 CNN_LSTM 改成 ConvLSTM
# 2. 應該把 loss and accuracy 視覺化
# 3. LSTM 的 prediction 就是要 predict 一整個 batch 的量。好消息是，tensorflow 可以共享 weight，所以可以先儲存 weight 在另外一個 graph 使用這個 weight，然後對 batch = 1 做 prediction。

# batch and epoch
'''

'''

# Procedure:
# 1. scrape finance data from yahoo finance
# 2. scrape finance data from investing.com (now manually)
# 3. modify data to deal with NAN and repeat data problem
# 4. calculate volatilities
# 5. calculate movements (should have the option to select label or value in the future)
# 6. calculate rolling connectedness (should try to increase the speed in the future)
# 7. add rolling connectedness (used only when there is new connectedness)
# 8. Turn data into TFRecord format
# 9. train model (CNN, RNN, ConvLSTM)
# 10. predict movement (CNN, RNN, ConvLSTM)

# import required module
import json
import os
import time
import functions.f_about_path as fap

# count the elapsed time span, start time
start_time = time.time()

'''
the relationship bet. batch, epoches:
'''

# the pre-requisite
prerequisite = {

    # target_folder saves all the data to calculate connectedness
    "target_folder": "market_price",

    # The start_dt and end_dt define the periods to calculate the predicted connectedness which is going to be input of tensorflow
    "start_dt": "2010-11-19",
    "end_dt": "2020-06-18",

    # The maximum lag to make VAR calculation
    "maximum_lag": 14,
    # The number of periods to calculate one connectedness
    "periods_one_conn": 365,
    # predict_conns_periods means how forward predicted periods of connectedness
    "predict_conns_periods": 1,

    # The number of epoches
    "epochs": 200,
    # The number of elements in a batch
    "batch_size": 128,
    # The number of labels
    "label_size": 2,  # (up and down)

    # The conns_for_one_element defines how many periods in one element, which means how many conns match one movement
    "conns_for_one_element": 14,  # the time periods of LSTM

    # predict_movement_periods means how many periods to be predicted
    "predict_movement_periods": 14,

    # variable related to RNN (LSTM)
    "layer_num": 4,
    "n_hidden_units": 128,

    # variable related to gerenal setting of model (這邊還沒做好)
    "iscontinue": False,  # whether to keep training model
    "iscontinue_conn": False,  # whether to keep calculating rolling connectedness

    # predict target
    "predict_target": '^TWII_move'
    }

# save the Prerequisite
file_path = os.path.dirname(os.path.realpath(__file__))
parent_path = fap.f_parent_path(file_path)
path = parent_path + '/docs/' + 'Prerequisite.json'
with open(path, 'w') as outfile:
    json.dump(prerequisite, outfile)

# get the number of market prices and the num of elements of connectedness table
target_folder = prerequisite['target_folder']
save_path = './docs/' + target_folder
num_of_files = sum([len(files) for r, d, files in os.walk(save_path)])
num_table_elements = (num_of_files + 1) ** 2

'''
# scrape finance data from yahoo finance
print("scraping finance data")
import scrape_finance_data_yahoo

# modify data to deal with NAN and repeat data problem
print("modifying data")
import load_and_modify_data

# calculate volatilities
print("calculating volatilities")
import volatility

# calculate movements (should have the option to select label or value)
print("calculating movements")
import movement

# calculate rolling connectedness
if prerequisite["iscontinue_conn"]:
    print("add new rolling connectedness")
    import add_roll_conn
else:
    print("calculating rolling connectedness")
    import roll_conn
'''

# Turn data into TFRecord format (這部分應該要先放棄，因為官方也說不清楚怎麼用tfrecord訓練模型)
'''
print("turning data format into TFRecord")
import data_TFRecord_format
'''

# train model CNN (還在 version1)
'''
print("training model CNN")
import train_model_CNN
'''

# train model RNN (正在改成 version2 的 keras)
print("training model RNN")
import train_model_RNN

# train model CNN_RNN (ConvLSTM) (還在 version1)
'''
print("training model CNN + RNN")
import train_model_CNN_RNN
'''

# make prediction CNN

'''
# make prediction RNN
print("make prediction")
import predict_RNN
'''

# make prediction ConvLSTM


# count the elapsed time span, end time
elapsed_time = time.time() - start_time
print("the time span in all procedure: ", elapsed_time)
print("===================")