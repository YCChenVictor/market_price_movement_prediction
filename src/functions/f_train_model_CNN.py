import tensorflow as tf
import os
import functions.about_path as fap
import json

#
#
#
#
#
# import prerequisite
file_path = os.path.dirname(os.path.realpath(__file__))
parent_path = fap.f_parent_path(file_path, 1)
path = parent_path + "/docs/" + "Prerequisite.json"
with open(path) as f:
    prerequisite = json.load(f)

# The variable from prerequsite
label_size = prerequisite["label_size"]

# get the number of instrumnets
target_folder = prerequisite["target_folder"]
file_path = os.path.dirname(os.path.realpath(__file__))
parent_path = fap.f_parent_path(file_path, 1)
save_path = parent_path + "/docs/" + target_folder
n_instruments = sum([len(files) for r, d, files in os.walk(save_path)])


#
#
#
#
# tfrecords
def read_and_decode(filename, batch_size, num_of_epoches):

    # produce the file queue
    filename_queue = tf.train.string_input_producer(
        [filename], shuffle=False, num_epochs=num_of_epoches
    )

    # The tool to read data from Train.tfrecords
    reader = tf.TFRecordReader()
    _, serialized_example = reader.read(filename_queue)

    # unpack tfrecords
    """
    The steps in packing TFRecord file:
    original file > Feature > Features > Example > TFRecord

    The steps in unpacking TFRecord file:
    TFRecord > Example > Features > Feature > original file

    Use tf.parse_single_example to turn tf.train.Example into
    tf.train.Features

    Use tf.decode_raw or tf.cast to turn tf.train.Features into
    tf.train.Feature
    """
    features = {
        "output": tf.FixedLenFeature([], tf.int64),
        "input": tf.FixedLenFeature([], tf.string),
    }

    data_features = tf.parse_single_example(serialized_example, features=features)

    input_tensor = tf.decode_raw(data_features["input"], tf.float32)

    input_tensor = tf.reshape(input_tensor, [n_instruments + 1, n_instruments + 1])

    output_tensor = tf.cast(data_features["output"], tf.int64)

    # output data in order / output data in random
    # tf.train.batch / tf.train.shuffle_batch
    input_batch, output_batch = tf.train.batch(
        [input_tensor, output_tensor],
        batch_size=batch_size,
        # capacity=10000 + 3 * batch_size,
        # min_after_dequeue=1000
    )

    return input_batch, output_batch

    # parameters of tf.train.shuffle_batch:
    # tensor: input_tensor and output_tensor
    # batch_size：The number of elements in a batch
    # capacity: must be int, the maximum number of element
    # min_after_dequeue： must be int, the minimum number remained after output
    # all the data


#
#
#
#
# tensors
def Weight(shape, mean=0, stddev=1):
    """
    If shape = [5, 5, 1, 4], the size of tensor that data going to input will
    be width=5, height=5, color=1, number of tensor = 4
    """
    # 以常態分佈進行初始化
    init = tf.truncated_normal(shape, mean=mean, stddev=stddev)

    # 以隨機分佈進行初始化
    # init = tf.random_normal(shape, mean=mean, stddev=stddev)

    return tf.Variable(init)


def bias(shape, mean=0, stddev=1):
    """
    the shape of bias must match the fourth element of the shape of Weight
    """
    init = tf.truncated_normal(shape, mean=mean, stddev=stddev)
    return tf.Variable(init)


# 預定義卷積運算子
def conv2d(x, W, strides=[1, 1, 1, 1]):
    """
    If [1, 1, 1, 1], means the step in width, height, color, tensor will be
    all 1
    """
    return tf.nn.conv2d(x, W, strides=strides, padding="SAME")


def max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1]):
    return tf.nn.max_pool(x, ksize=ksize, strides=strides, padding="SAME")


# function for neural network
def neural_network_model(x):

    # The tensors to calculate prediction (y)
    # Construct Convolution
    # Conv1
    W_conv1 = Weight([10, 10, 1, 16])
    b_conv1 = bias([16])
    y_conv1 = conv2d(x, W_conv1) + b_conv1

    # ReLU1
    relu1 = tf.nn.relu(y_conv1)

    # Pool1
    pool1 = max_pool(relu1)

    # Conv2
    W_conv2 = Weight([6, 6, 16, 32])
    b_conv2 = bias([32])
    y_conv2 = conv2d(pool1, W_conv2) + b_conv2

    # ReLU2
    relu2 = tf.nn.relu(y_conv2)

    # Pool2
    pool2 = max_pool(relu2)

    # FC1
    W_fc1 = Weight([128 * 16, 64])  # 這邊一直有問題，到底要多少數字？
    b_fc1 = bias([64])
    h_flat = tf.reshape(pool2, [-1, 128 * 16])
    y_fc1 = tf.matmul(h_flat, W_fc1) + b_fc1

    # ReLU3
    relu3 = tf.nn.relu(y_fc1)

    # FC2 - output layer
    W_fc2 = Weight([64, label_size])
    b_fc2 = bias([label_size])

    y = tf.matmul(relu3, W_fc2) + b_fc2

    return y
