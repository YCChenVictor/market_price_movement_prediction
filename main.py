# conclusion:
# 1. CNN cannot be used (training accuracy cannot increase)
# 2. LSTM can still be used (training accuracy can reach 100%)
# 3. Convert CNN_LSTM to ConvLSTM

# problem:
# 1. Change CNN_LSTM to ConvLSTM
# 2. Visualize loss and accuracy
# 3. For LSTM prediction, predict the entire batch. Good news is that TensorFlow can share weights, so you can save the weights and use them in another graph to predict batch = 1.

# batch, epoch & iteration
'''
epoch: When a complete dataset passes through a neural network and returns once, this process is called one epoch.
batch: When it is not possible to pass the entire dataset through the neural network at once, the dataset is divided into several batches.
iteration: An iteration is the number of times a batch needs to be completed to complete one epoch.

For example, if there is a dataset with 2000 training samples and it is divided into batches of size 500, then it would take 4 iterations to complete one epoch.
'''

# Procedure:
# 1. scrape finance data from yahoo finance
# 2. scrape finance data from investing.com (now manually)
# 3. modify data to deal with NAN and repeat data problem
# 4. calculate volatility
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

# save the Prerequisite
file_path = os.path.dirname(os.path.realpath(__file__))
parent_path = fap.f_parent_path(file_path)
path = parent_path + 'Prerequisite.json'
with open(path, 'w') as outfile:
    json.dump(prerequisite, outfile)

# get the number of market prices and the num of elements of connectedness table
target_folder = prerequisite['target_folder']
save_path = './docs/' + target_folder
num_of_files = sum([len(files) for r, d, files in os.walk(save_path)])
num_table_elements = (num_of_files + 1) ** 2

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

# Turn data into TFRecord format (這部分應該要先放棄，因為官方也說不清楚怎麼用tfrecord訓練模型)
print("turning data format into TFRecord")
import data_TFRecord_format

# train model CNN (還在 version1)
'''
print("training model CNN")
import train_model_CNN
'''

# train model RNN
'''
這邊要設計一個依照上次checkpoint後繼續training的選項
print("training model RNN")
import train_model_RNN
'''

# train model CNN_RNN (ConvLSTM) (還在 version1)
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