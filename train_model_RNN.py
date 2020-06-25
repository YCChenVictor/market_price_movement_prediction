'''keras tutorial: https://www.tensorflow.org/guide/keras/functional'''

import tensorflow as tf
from functions.f_train_model_RNN import (extract_features, get_batched_dataset, get_model)
import os
import functions.f_about_path as fap
import json
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import math
from tensorflow import keras
import functions.f_date as ffd
import pickle
import numpy as np

# The Prerequisite, n_instruments, tfrecords file ####
# import prerequiste
file_path = os.path.dirname(os.path.realpath(__file__))
parent_path = fap.f_parent_path(file_path)
pre_path = parent_path + '/docs/' + 'Prerequisite.json'
with open(pre_path) as f:
    prerequisite = json.load(f)

# The variable from prerequsite
batch_size = prerequisite["batch_size"]
conns_for_one_element = prerequisite["conns_for_one_element"]
epochs = prerequisite["epochs"]
n_hidden_units = prerequisite["n_hidden_units"]

# get the number of price
target_folder = prerequisite['target_folder']
file_path = os.path.dirname(os.path.realpath(__file__))
path = file_path + '/docs/' + target_folder
n_price = sum([len(files) for r, d, files in os.walk(path)])

# the number of elements in a connectedness table
n_table_elements = (n_price + 1) ** 2

# The TFRecord file path (放棄使用tfrecord)
# filename = './docs/py_Train_flat.tfrecords'

# read input_dict and output_dict for training
with open('./docs/input_dict.pickle', 'rb') as f:
    input_dict = pickle.load(f)
with open('./docs/output_dict.pickle', 'rb') as f:
    output_dict = pickle.load(f)

# append input_dict
input_list = []
for key, item in input_dict.items():
    input_list.append(item)
X_train = np.array(input_list) # [samples, timesteps, features]

# append output_dict
output_list = []
for key, item in output_dict.items():
    output_list.append(item)
y_train = np.array(output_list)
y_train = y_train.reshape((y_train.shape[0],))

# training loop ####
# define model
model = get_model(conns_for_one_element, n_table_elements, n_hidden_units)
# fit the model
model.fit(X_train, y_train, epochs=350, batch_size=32, verbose=2)
'''
# evaluate the model
mse, mae = model.evaluate(X_test, y_test, verbose=0)
print('MSE: %.3f, RMSE: %.3f, MAE: %.3f' % (mse, sqrt(mse), mae))
# make a prediction
row = asarray([18024.0, 16722.0, 14385.0, 21342.0, 17180.0]).reshape((1, n_steps, 1))
yhat = model.predict(row)
print('Predicted: %.3f' % (yhat))
'''