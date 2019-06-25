import tensorflow as tf
from functions.f_train_model_RNN import (read_and_decode,
                                         neural_network_model,
                                         train_RNN,
                                         neural_network_model)
import os
import functions.about_path as fap
import json
# import sys
# import numpy
# numpy.set_printoptions(threshold=sys.maxsize)
#
#
#
#
#
# The Prerequisite, n_instruments, tfrecords file ####
# import prerequiste
file_path = os.path.dirname(os.path.realpath(__file__))
parent_path = fap.f_parent_path(file_path)
pre_path = parent_path + '/docs/' + 'Prerequisite.json'
with open(pre_path) as f:
    prerequisite = json.load(f)

# The variable from prerequsite
batch_size = prerequisite["batch_size"]
label_size = prerequisite["label_size"]
conns_for_one_element = prerequisite["conns_for_one_element"]
max_epoches = prerequisite["max_epoches"]
layer_num = prerequisite["layer_num"]
n_hidden_units = prerequisite["n_hidden_units"]
iscontinue = prerequisite["iscontinue"]

# get the number of instrumnets
target_folder = prerequisite['target_folder']
file_path = os.path.dirname(os.path.realpath(__file__))
path = file_path + '/docs/' + target_folder
n_instruments = sum([len(files) for r, d, files in os.walk(path)])

# the number of elements in a connectedness table
n_table_elements = (n_instruments + 1) ** 2

# the number of input and output pairs


# The TFRecord file path
filename = './docs/py_Train_flat.tfrecords'
#
#
#
#
#
# The tensors related to training ####

# Input & Output (true data)
x = tf.placeholder(tf.float32, shape=[None, conns_for_one_element,
                                      n_table_elements])
'''
conns_for_one_element stands for number of timestep
'''
y_ = tf.placeholder(tf.float32, shape=[None, label_size])

# setting prob for dropoutwrapper
keep_prob = tf.placeholder(tf.float32)

# setup the source of input data
input_batch, output_batch = read_and_decode(filename, batch_size,
                                            max_epoches,
                                            conns_for_one_element,
                                            n_table_elements)
train_x = tf.reshape(input_batch, [-1, conns_for_one_element,
                                   n_table_elements])
train_y = tf.one_hot(output_batch, label_size)

# LSTM neural_network
y = neural_network_model(x, layer_num, n_hidden_units, batch_size,
                         label_size, n_table_elements,
                         conns_for_one_element, keep_prob)

# calcute the position of maximum value in y
y_pred = tf.argmax(y, 1)

# function to calculate Cost
lossFcn = tf.nn.softmax_cross_entropy_with_logits_v2
cost = tf.reduce_mean(lossFcn(labels=y_, logits=y))

# use AdamOptimizer to minimize cost
optimizer = tf.train.AdamOptimizer(0.001).minimize(cost)

# calculate accuracy
correct_prediction = tf.equal(tf.argmax(y_, 1), tf.argmax(y, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

# collect the parameter for future prediction
tf.add_to_collection('input', x)
tf.add_to_collection('output', y_pred)
tf.add_to_collection('keep_prob', keep_prob)
#
#
#
#
#
# Start the training ####

# construt tf.train.Saver
saver = tf.train.Saver()

# the saving path
save_path = './model_RNN/tf_trained_model'

with tf.Session() as sess:

    # Initializing
    sess.run(tf.local_variables_initializer())
    sess.run(tf.global_variables_initializer())

    # Construct Coordinator
    coord = tf.train.Coordinator()

    # Start the file queue and read file
    threads = tf.train.start_queue_runners(coord=coord)

    # the path to save the count
    file_path = os.path.dirname(os.path.realpath(__file__))
    parent_path = fap.f_parent_path(file_path)
    post_path = parent_path + '/docs/' + 'post_requisite.json'

    count_save_path = post_path

    with open(post_path) as f:
        post_requisite = json.load(f)

    # start the training
    if iscontinue:  # whether to continue the past training

        # import the graph from the file
        last_ckp = tf.train.latest_checkpoint("./model_RNN")
        imported_graph = tf.train.import_meta_graph(last_ckp + '.meta')
        imported_graph.restore(sess, last_ckp)

        count = post_requisite["train_time"]

        train_RNN(coord, sess, train_x, train_y, optimizer, x, y_, accuracy,
                  saver, save_path, count_save_path, count, cost, keep_prob)

    else:
        count = 1
        train_RNN(coord, sess, train_x, train_y, optimizer, x, y_, accuracy,
                  saver, save_path, count_save_path, count, cost, keep_prob)
