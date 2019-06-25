import tensorflow as tf
from functions.f_train_model_CNN import (read_and_decode, neural_network_model)
import os
import functions.about_path as fap
import json
import numpy as np
#
#
#
#
#
# The Prerequisite, n_instruments, tfrecords file ####
# import prerequiste
file_path = os.path.dirname(os.path.realpath(__file__))
parent_path = fap.f_parent_path(file_path)
path = parent_path + '/docs/' + 'Prerequisite.json'
with open(path) as f:
    prerequisite = json.load(f)

# import Post_requisite
path = parent_path + '/docs/' + 'Post_requisite.json'
with open(path) as f:
    Post_requisite = json.load(f)

# The variable from prerequsite
batch_size = prerequisite["batch_size"]
label_size = prerequisite["label_size"]
num_of_features = Post_requisite["num_of_features"]
num_of_epoches = prerequisite["num_of_epoches"]

# get the number of instrumnets
target_folder = prerequisite['target_folder']
file_path = os.path.dirname(os.path.realpath(__file__))
path = file_path + '/docs/' + target_folder
n_instruments = sum([len(files) for r, d, files in os.walk(path)])

# the number of elements in a connectedness table
n_table_elements = (n_instruments + 1) ** 2

# the number of input and output pairs


# The TFRecord file path
filename = './docs/py_Train.tfrecords'
#
#
#
#
#
# The tensors related to training ####
'''
The basic steps in CNN: Conv -> ReLu -> Pool

After the steps in CNNs, Full Connect (FC) comes

In the below code, there will be two CNN layers followed by two FC
'''

# The tensors to place true data, x for input, y_ for output
x = tf.placeholder(tf.float32, shape=[None, n_instruments+1,
                                      n_instruments+1, 1])
y_ = tf.placeholder(tf.float32, shape=[None, label_size])
'''
x and y_ is going to input train_x and train_y
'''
#
#
# The tensors to calculate prediction (y)
y = neural_network_model(x)
#
#
# tensors related to train model
# Cost optimizer
lossFcn = tf.nn.softmax_cross_entropy_with_logits_v2
cost = tf.reduce_mean(lossFcn(labels=y_, logits=y))

# use AdamOptimizer to minimize the cost
optimizer = tf.train.AdamOptimizer(0.001).minimize(cost)

# calculate accuracy
correct_prediction = tf.equal(tf.argmax(y_, 1), tf.argmax(y, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
#
#
# setup the data source (from tfrecord, with batch setting)
input_batch, output_batch = read_and_decode(filename, batch_size,
                                            num_of_epoches)
train_x = tf.reshape(input_batch, [-1, n_instruments+1,
                                   n_instruments+1, 1])
train_y = tf.one_hot(output_batch, label_size)

# calcute the position of maximum value in y
y_pred = tf.argmax(y, 1)

# construt tf.train.Saver
saver = tf.train.Saver()

# collect the input and output data
tf.add_to_collection('input', x)
tf.add_to_collection('output', y_pred)
#
#
#
#
#
# Start the training ####
with tf.Session() as sess:

    # Initializing
    sess.run(tf.local_variables_initializer())
    sess.run(tf.global_variables_initializer())

    # Construct Coordinator
    coord = tf.train.Coordinator()

    # Start the file queue and read file
    threads = tf.train.start_queue_runners(coord=coord)

    # start the training
    save_path = './model_CNN/tf_trained_model'
    count = 1
    batch = 1
    epoch = 1
    try:
        while not coord.should_stop():

            input_data, output_data = sess.run([train_x, train_y])
            # print(np.shape(input_data))
            # print(np.shape((output_data)))

            # start training
            sess.run(optimizer, feed_dict={x: input_data,
                                           y_: output_data})

            # calculate accuracy
            train_accuracy = accuracy.eval({x: input_data,
                                            y_: output_data})

            # print out accuracy
            print("Training accuracy %g in batch %d of epoch %d" %
                  (train_accuracy, epoch, batch))

            count = count + 1

            batch = batch + 1

            # epoch + 1 once all the data run once (all the batches run once)
            if batch > num_of_features/batch_size:
                epoch = epoch + 1
                batch = 1

            # save the training result
            spath = saver.save(sess, save_path, global_step=count)
            print("Model saved in file: %s" % spath)

            # print(count)
            # print(batch)
            # print(epoch)

        # save the trained session
        saver.save(sess, "check_point/model.ckpt")

        # save all the session
        spath = saver.save(sess, save_path)
        print("Model saved in file: %s" % spath)

    # If num_epochs run out => error
    except tf.errors.OutOfRangeError:
        print("---Train end---")

    finally:
        # terminate coord
        coord.request_stop()
        print('---Programm end---')
        # addd the trained line to threads
