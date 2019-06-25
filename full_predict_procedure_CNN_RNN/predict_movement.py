"""
Try to use TFRecord method
"""

# import required modules
import os
import pickle
import tensorflow as tf
from functions.f_predict_movement import (train_predict_split,
                                          train_neural_network,
                                          predict_neural_network)
import time
import functions.about_path as fap
import json


# count the elapsed time span, start time
start_time = time.time()

tf.random.set_random_seed(1)  # so that the result can be reproducable


# import prerequisite
file_path = os.path.dirname(os.path.realpath(__file__))
parent_path = fap.f_parent_path(file_path)
path = parent_path + '/docs/' + 'Prerequisite.json'
with open(path) as f:
    prerequisite = json.load(f)


# select the number of periods for one full training (back one year)
conns_for_one_batch = prerequisite["conns_for_one_batch"]

# choose how many periods to predict movements
predict_periods = prerequisite["predict_periods"]

# target folder to get the number of file
target_folder = prerequisite["target_folder"]

# simple version for working with CWD
file_path = os.path.dirname(os.path.realpath(__file__))
save_path = file_path + '/docs/' + target_folder
n_instrument = sum([len(files) for r, d, files in os.walk(save_path)])
# print(n_instrument)

# start training ####
# hyperparameters
# n_classes = 2  # up or down
hm_epochs = 1000

chunk_size = (n_instrument+1)**2  # the data size of x in each date
# print(chunk_size)

n_chunks = conns_for_one_batch  # the number of diff_conn in one batch

rnn_size = chunk_size * n_chunks

x = tf.placeholder('float', [n_chunks, chunk_size], name="x")
y = tf.placeholder('float', name='y')


# define layer form: every layer has weight and biases. the dimension of
# //input is rnn_size, and the output is the number of classes, n_classes.
layer = {'weights': tf.Variable(tf.random_normal([rnn_size, 1]),
         name='weights'),
         'biases': tf.Variable(tf.random_normal([1]), name='biases')}


# create file to save the session run and the number of epoch
saver = tf.train.Saver()  # it will save the variables of the layer
tf_log = 'tf_log'


# path to save epoch loss
file_path = os.path.dirname(os.path.realpath(__file__))
save_path = file_path + '/docs/' + 'epoch_loss.pickle'


# import data (inputs_outputs)
file_path = os.path.dirname(os.path.realpath(__file__))
save_path = file_path + '/docs/' + 'inputs_outputs.pickle'
with open(save_path, 'rb') as f:
    inputs_outputs = pickle.load(f)


# split train dataset and test dataset (defalut 1 periods testing)
train_dict, test_dict = train_predict_split(inputs_outputs, predict_periods)


# train the model
train_neural_network(x, y, tf_log, hm_epochs, saver, inputs_outputs,
                     chunk_size, n_chunks, rnn_size, layer, save_path)

# make prediction
predict_neural_network(x, y, chunk_size, n_chunks, rnn_size, layer,
                       hm_epochs, saver, test_dict)


# count the elapsed time span, end time
elapsed_time = time.time() - start_time
print("the time span in perdicting movement: ", elapsed_time)
print("===================")
