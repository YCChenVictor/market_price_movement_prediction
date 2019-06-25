import tensorflow as tf
import numpy as np
import os
import json
import datetime
import random
import functions.f_date as fd
import functions.about_path as fap


# function to turn Int64 into 'tf.train.Feature' format
def int64_feature(value):
    if not isinstance(value, list):
        value = [value]
    return tf.train.Feature(int64_list=tf.train.Int64List(value=value))


# function to turn Bytes into 'tf.train.Feature' format
def bytes_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))


# function to turn float inro 'tf.train.Feature' format
def float_feature(value):
    return tf.train.Feature(float_list=tf.train.FloatList(value=value))


# functions to convert input and output data into TFRecord
def convert_to_TFRecord(inputs, outputs, filename):

    TFWriter = tf.python_io.TFRecordWriter(filename)
    print('\nTransform start...')

    num_of_data = 0
    for key, item in inputs.items():

        try:
            # print(key)
            # print(inputs[key])
            # print(outputs[key])

            # input & output
            input_single = inputs[key].tostring()
            # print(input_single)
            output_single = int(outputs[key])
            # print(output_single)

            # turn input and output into tf.train.Feature
            input_tf = bytes_feature(input_single)
            # print(input_tf)
            output_tf = int64_feature(output_single)
            # print(output_tf)

            # combine tf.train.Feature into tf.train.Features
            tf_features = tf.train.Features(
                   feature={'output': output_tf,
                            'input': input_tf})

            # turn tf.train.Features into tf.train.Example
            example = tf.train.Example(features=tf_features)
            # print(example)

            # write tf.train.Example as tfRecord format
            TFWriter.write(example.SerializeToString())

            # updates num_of_features
            num_of_data = num_of_data + 1

            # print(num_of_features)

        except IOError as e:
            print(e)
            print('Skip!\n')

    # save the number of data
    file_path = os.path.dirname(os.path.realpath(__file__))
    parent_path = fap.f_parent_path(file_path, 1)
    path = parent_path + '/docs/' + 'post_requisite.json'

    post_requisite = {}

    post_requisite["num_of_data"] = num_of_data

    # save it into post_requisite
    with open(path, 'w') as outfile:
        json.dump(post_requisite, outfile)

    # print(prerequisite)

    TFWriter.close()
    print('Transform done!')


# function to split dict into train and test
def split_dict_train_test(dict_data, predict_movement_periods):

    # dict for train and test dataset
    train_dict = {}
    test_dict = {}

    i = 0

    # list for key going to be deleted
    key_delete_list = []

    # add data into train_dict
    for key, item in dict_data.items():

        # append it into train_dict
        train_dict[key] = item

        # add key into delete list
        key_delete_list.append(key)

        i = i + 1

        if i == (len(dict_data.keys()) - predict_movement_periods):
            break

    # delete the data in train_dict
    for key in key_delete_list:

        del dict_data[key]

    # add data into test_dict
    for key, item in dict_data.items():

        test_dict[key] = item

    return train_dict, test_dict


# create elements for ConvLSTM
def conn_table_periods_converter(table_dict, periods):

    # get the key list
    key_list = list(table_dict.keys())
    # print(key_list)

    # target
    data_dict = {}

    # divide the keys iteratively according to periods
    for key in range(len(key_list)):

        # obtain the last periods of key
        last_keys = key_list[-(periods+1): -1]
        # print(last_keys)

        # delete the last key
        del key_list[-1]

        # if the length is lower than periods
        if len(key_list) < periods + 1:
            break

        # get the element from dict
        target = np.array([table_dict[x].values for x in last_keys])

        # add into dict
        data_dict[key] = target

    # get the key list
    key_list = list(table_dict.keys())

    data_dict_date = {}

    for key, item in data_dict.items():

        # get the date ##
        # convert date into date_format
        date = datetime.datetime.combine(fd.date_format(key_list[key]),
                                         datetime.time())

        # add periods days
        date = date + datetime.timedelta(days=periods)

        data_dict_date[date] = item

    return data_dict_date


# function to delete extra data in output_dict
def input_output_same_key(input_dict, output_dict):

    # get output_dict according to input_dict_key
    output_dict_new = {}

    for key, item in input_dict.items():
        output_dict_new[key] = output_dict[key]

    return input_dict, output_dict_new


# function to balance labels (avoid prediction bias)
def balance_label(input_dict, output_dict):

    # get the input_dict and output_dict keys
    key_list_0 = []
    key_list_1 = []

    for key, item in output_dict.items():

        if item is 0:
            key_list_0.append(key)
        else:
            key_list_1.append(key)

    # compare which is longer and modify to the same
    if len(key_list_0) > len(key_list_1):
        key_list_0 = random.sample(key_list_0, len(key_list_1))
    else:
        key_list_1 = random.sample(key_list_1, len(key_list_1))

    # create new input_dict
    input_dict_new = {}

    for key in key_list_0:
        input_dict_new[key] = input_dict[key]

    for key in key_list_1:
        input_dict_new[key] = input_dict[key]

    return input_dict_new, output_dict


# function to shuffle the input (output shuffled in tfrecord accordingly)
def shuffle_input_dict(input_dict):

    # shuffle keys
    key_list = list(input_dict.keys())
    random.shuffle(key_list)

    input_dict_shuffle = {}
    for key in key_list:
        input_dict_shuffle[key] = input_dict[key]

    return input_dict_shuffle
