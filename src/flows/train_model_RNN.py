import tensorflow as tf
from functions.f_train_model_RNN import extract_features, get_batched_dataset, get_model
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
pre_path = parent_path + "/docs/" + "Prerequisite.json"
with open(pre_path) as f:
    prerequisite = json.load(f)

# The variable from prerequsite
batch_size = prerequisite["batch_size"]
conns_for_one_element = prerequisite["conns_for_one_element"]
epochs = prerequisite["epochs"]
n_hidden_units = prerequisite["n_hidden_units"]

# get the number of price
target_folder = prerequisite["target_folder"]
file_path = os.path.dirname(os.path.realpath(__file__))
path = file_path + "/docs/" + target_folder
n_price = sum([len(files) for r, d, files in os.walk(path)])

# the number of elements in a connectedness table
n_table_elements = (n_price + 1) ** 2

# The TFRecord file path (放棄使用tfrecord)
# filename = './docs/py_Train_flat.tfrecords'

# read input_dict and output_dict for training
with open("./docs/input_dict_train.pickle", "rb") as f:
    input_dict_train = pickle.load(f)
with open("./docs/output_dict_train.pickle", "rb") as f:
    output_dict_train = pickle.load(f)
with open("./docs/input_dict_test.pickle", "rb") as f:
    input_dict_test = pickle.load(f)
with open("./docs/output_dict_test.pickle", "rb") as f:
    output_dict_test = pickle.load(f)

# append input_dict_train
input_list_train = []
for key, item in input_dict_train.items():
    input_list_train.append(item)
X_train = np.array(input_list_train)  # [samples, timesteps, features]

# append output_dict_train
output_list_train = []
for key, item in output_dict_train.items():
    output_list_train.append(item)
y_train = np.array(output_list_train)
y_train = y_train.reshape((y_train.shape[0],))  # [lebal, ]

# append output_dict_test
output_list_test = []
for key, item in output_dict_test.items():
    if item == None:
        key_future = key
        continue
    else:
        output_list_test.append(item)
y_test = np.array(output_list_test)
y_test = y_test.reshape((y_test.shape[0],))  # [lebal, ]

# append input_dict_test
input_list_test = []
for key, item in input_dict_test.items():
    if key == key_future:
        continue
    else:
        input_list_test.append(item)
X_test = np.array(input_list_test)  # [samples, timesteps, features]

# training loop ####
"""https://machinelearningmastery.com/tensorflow-tutorial-deep-learning-with-tf-keras/"""
# define model
"""https://www.tensorflow.org/tutorials/keras/save_and_load"""
# checkpoint
checkpoint_path = "./docs/checkpoint/cp.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)
# Create a callback that saves the model's weights
cp_callback = tf.keras.callbacks.ModelCheckpoint(
    filepath=checkpoint_path, save_weights_only=True, verbose=2
)
# define the model structure
model = get_model(conns_for_one_element, n_table_elements, n_hidden_units)
# fit the model
model.fit(
    X_train,
    y_train,
    epochs=epochs,
    batch_size=batch_size,
    verbose=2,
    # validation_data=(X_test, y_test),
    callbacks=[cp_callback],
)
