from tensorflow.python import keras as keras
import tensorflow as tf
import os
import json
import functions.about_path as fap


# import prerequiste
file_path = os.path.dirname(os.path.realpath(__file__))
parent_path = fap.f_parent_path(file_path, 1)
path = parent_path + '/docs/' + 'Prerequisite.json'
with open(path) as f:
    prerequisite = json.load(f)


# tfrecords
def read_and_decode(filename, batch_size, num_of_epoches, periods,
                    n_instruments):

    # produce the file queue
    filename_queue = tf.train.string_input_producer([filename],
                                                    shuffle=False,
                                                    num_epochs=num_of_epoches)

    # The tool to read data from Train.tfrecords
    reader = tf.TFRecordReader()
    _, serialized_example = reader.read(filename_queue)

    # unpack tfrecords
    '''
    The steps in packing TFRecord file:
    original file > Feature > Features > Example > TFRecord

    The steps in unpacking TFRecord file:
    TFRecord > Example > Features > Feature > original file

    Use tf.parse_single_example to turn tf.train.Example into
    tf.train.Features

    Use tf.decode_raw or tf.cast to turn tf.train.Features into
    tf.train.Feature
    '''
    features = {'output': tf.FixedLenFeature([], tf.int64),
                'input': tf.FixedLenFeature([], tf.string)}

    data_features = tf.parse_single_example(serialized_example,
                                            features=features)

    input_tensor = tf.decode_raw(data_features['input'], tf.float32)

    input_tensor = tf.reshape(input_tensor, [periods, n_instruments + 1,
                                             n_instruments + 1])

    output_tensor = tf.cast(data_features['output'], tf.int64)

    # output data in order / output data in random
    # tf.train.batch / tf.train.shuffle_batch
    input_batch, output_batch = tf.train.batch(
        [input_tensor, output_tensor],
        batch_size=batch_size
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


def neural_network_CNN():

    # construct cnn
    model = keras.Sequential()

    # first conv layer
    model.add(keras.layers.Conv2D(filters=32,
                                  kernel_size=(10, 10),
                                  # strides=1,
                                  padding='same',
                                  # input_shape=(31, 31, 1),
                                  activation='relu'))
    '''
    filters: the number of conv to be produced
    kernel_size: the hight and width of produced conv
    input_shape: the shape of the image input (here, table shape)
    '''
    model.add(keras.layers.MaxPooling2D(pool_size=(2, 2)))
    '''
    沿（垂直，水平）方向缩小比例的因数
    '''

    # flatten
    model.add(keras.layers.Flatten())

    # full Connect
    model.add(keras.layers.Dense(128, activation='relu'))

    return model


def neural_network_CNN_RNN(x, time_step, cnn=neural_network_CNN()):

    # Combine it with keras
    model_input = keras.layers.Input(tensor=x)

    # distribute cnn to RNN
    model_output = (keras.layers.
                    TimeDistributed(cnn,
                                    input_shape=(time_step, 31, 31, 1))(model_input))

    # construct LSTM layer
    model_output = keras.layers.LSTM(time_step)(model_output)

    # construct Dense layer
    model_output = keras.layers.Dense(128)(model_output)

    return model_output
