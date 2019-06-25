# general note:
'''
1. 如果有 1000 個樣本，batch_size = 10，完整訓練一次需要 100 次 iteration，一次 epoch
'''
# conclusion:
'''
1. CNN 不能用（training accuracy 無法上升）
2. LSTM 還可以用（training accuracy 可以上到 100%）
3. CNN_LSTM 真的寫不出來，目前有點來不及了，然後我發現有 ConvLSTM...

除非能找到使 CNN 的 training accuracy 上升的方法，不然做 ConvLSTM 好像沒什麼用
現在直接用 LSTM 做 prediction
'''
# problem:
'''
1. 把 CNN_LSTM 改成 ConvLSTM
2. If I change it into multi-layer RNN, the prediction is strange. 好像是 dropout layer 造成的，這要多了解
3. 應該把 loss and accuracy 視覺化
4. 試著去知道正統的 prediction 是怎麼用的
5. 深深的覺得要花時間去上課
6. LSTM 的 prediction 就是要 predict 一整個 batch 的量。好消息是，tensorflow 可以共享 weight，所以可以先儲存 weight 在另外一個 graph 使用這個 weight，然後對 batch = 1 做 prediction。
'''
#
#
# import required module
import json
import os
import functions.about_path as about_path
import time
import functions.about_path as fap


# Procedure:
'''
1. scrape finance data from yahoo finance
2. scrape finance data from investing.com (now manually)
3. modify data to deal with NAN and repeat data problem
4. calculate volatilities
5. calculate movements (should have the option to select label or value)
6. calculate rolling connectedness
7. add rolling connectedness (used only when there is new connectedness)
8. Turn data into TFRecord format
9. train model (CNN, RNN, ConvLSTM)
10. predict movement (CNN, RNN, ConvLSTM)
'''


# count the elapsed time span, start time
start_time = time.time()


# the pre-requisite
prerequisite = {

    # target_folder saves all the data to calculate connectedness
    "target_folder": "all",

    # The start_dt and end_dt define the periods to calculate the predicted
    # //connectedness
    "start_dt": "2009-1-29",
    "end_dt": "2019-1-29",

    # The maximum lag to make VAR calculation
    "maximum_lag": 14,
    # The number of periods to calculate one connectedness
    "periods_one_conn": 365 * 2,
    # predict_conns_periods means how forward predicted periods of
    # //connectedness
    "predict_conns_periods": 1,

    # The number of epoches
    "max_epoches": None,
    # The number of elements in a batch
    "batch_size": 128,
    # The number of labels
    "label_size": 2,  # (up and down)

    # The conns_for_one_element defines how many periods in one element, which
    # //means how many conns match one movement
    "conns_for_one_element": 14,  # it should be the time periods of LSTM

    # predict_movement_periods means how many periods to be predicted
    "predict_movement_periods": 128,

    # variable related to RNN
    "layer_num": 4,
    "n_hidden_units": 128,

    # variable related to gerenal setting of model
    "iscontinue": True,

    # predict target
    "predict_target": '^TWII_move'
    }


# save the Prerequisite
file_path = os.path.dirname(os.path.realpath(__file__))
parent_path = about_path.f_parent_path(file_path)
path = parent_path + '/docs/' + 'Prerequisite.json'
with open(path, 'w') as outfile:
    json.dump(prerequisite, outfile)

'''
# save the post_repuisite
path = parent_path + '/docs/' + 'Post_requisite.json'
with open(path, 'w') as outfile:
    json.dump(post_requisite, outfile)
'''

# get the number of instrumnets
target_folder = prerequisite['target_folder']
file_path = os.path.dirname(os.path.realpath(__file__))
parent_path = fap.f_parent_path(file_path, 1)
save_path = parent_path + '/docs/' + target_folder
n_instruments = sum([len(files) for r, d, files in os.walk(save_path)])
n_table_elements = (n_instruments + 1) ** 2


# scrape finance data from yahoo finance
'''
print("scraping finance data")
import scrape_finance_data_yahoo
'''

# scrape finance data from investing.com (now manually)


# modify data to deal with NAN and repeat data problem
'''
print("modifying data")
import load_and_modify_data
'''


# calculate volatilities
'''
print("calculating volatilities")
import volatility
'''


# calculate movements (should have the option to select label or value)
'''
print("calculating movements")
import movement
'''


# calculate rolling connectedness
'''
print("calculating rolling connectedness")
import roll_conn
'''

# add rolling connectedness (used only when there is new connectedness)
'''
print("add new rolling connectedness")
try:
    import add_roll_conn
except:
    pass
'''

# Turn data into TFRecord format
'''
print("turning data format into TFRecord")
import data_TFRecord_format
'''

# train model CNN
'''
print("training model CNN")
import train_model_CNN
'''

# train model RNN
'''
print("training model RNN")
import train_model_RNN
'''

# train model CNN_RNN (ConvLSTM)
'''
print("training model CNN + RNN")
import train_model_CNN_RNN
'''

# make prediction CNN

# make prediction RNN
print("make prediction")
import predict_RNN

# make prediction ConvLSTM


# count the elapsed time span, end time
elapsed_time = time.time() - start_time
print("the time span in all procedure: ", elapsed_time)
print("===================")
