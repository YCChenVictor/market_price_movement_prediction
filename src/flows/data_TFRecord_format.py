import time
import os
import functions.f_about_path as fap
import json
import pickle
import pandas as pd
import datetime
import functions.f_date as fd


from functions.f_rolling_connectedness import roll_conn_elements
from functions.f_TFRecord import (
    split_dict_train_test,
    input_output_same_key,
    balance_label,
    shuffle_input_dict,
)


# count the elapsed time span, start time
start_time = time.time()


# import prerequiste
file_path = os.path.dirname(os.path.realpath(__file__))
parent_path = fap.f_parent_path(file_path)
path = parent_path + "/docs/" + "Prerequisite.json"
with open(path) as f:
    prerequisite = json.load(f)
conns_for_one_element = prerequisite["conns_for_one_element"]
predict_movement_periods = prerequisite["predict_movement_periods"]


# import data
file_path = os.path.dirname(os.path.realpath(__file__))
move_path = file_path + "/docs/" + "movement.pickle"
roll_conn_flat_path = file_path + "/docs/" + "roll_conn_flat.pickle"
roll_conn_path = file_path + "/docs/" + "roll_conn.pickle"
with open(move_path, "rb") as f:
    movement = pickle.load(f)
with open(roll_conn_flat_path, "rb") as f:
    roll_conn_flat_dict = pickle.load(f)
with open(roll_conn_path, "rb") as f:
    roll_conn_dict = pickle.load(f)
#
#
#
#
#
# specify the movement we want to predict (For testing, specify Taiwan Stock)
# movement_names = list(movement)
# print(movement_names)

# predict_target = input("please select what market movement to predict: ")
# if predict_target not in movement_names:
#     print("error, please run again")
# else:
#     print("successfully select the target: " + predict_target)
predict_target = "^TWII_move"
movement_target = movement[predict_target]
movement_dict = movement_target.to_dict()  # output
#
#
#
#
#
# roll_conn_flat #### (for RNN)
# according to the conn_for_one_element, manipulate input data
conn_df = pd.concat(roll_conn_flat_dict)
conn_df = conn_df.reset_index().set_index("level_0").drop(["level_1"], axis=1)


# divide and difference the rolling conncetedness dataframe (input)
sliced_dict = roll_conn_elements(conn_df, conns_for_one_element)


# turn the rowname of sliced_dict from string into datetime so that it can be
# matched with movement_dict
roll_conn_flat_elements_dict = {
    datetime.datetime.combine(fd.date_format(key), datetime.time()): item
    for key, item in sliced_dict.items()
}

# split data into train and test dataset
train_flat_dict, test_flat_dict = split_dict_train_test(
    roll_conn_flat_elements_dict, predict_movement_periods
)

# deal with train dataset ####
# make the input and output dict the same keys (delete excess data in output)
input_dict_train, output_dict_train = input_output_same_key(
    train_flat_dict, movement_dict
)

# balance label (avoid tendency to predict only one label)
input_dict_train, output_dict_train = balance_label(input_dict_train, output_dict_train)

# shuffle the input (output shuffled in tfrecord accordingly with the key in
# convert_to_TFRecord)
input_dict_train, output_dict_train = shuffle_input_dict(
    input_dict_train, output_dict_train
)

# deal with test dataset ####
# make the input and output dict the same keys (delete excess data in output)
input_dict_test, output_dict_test = input_output_same_key(test_flat_dict, movement_dict)

# balance label (avoid tendency to predict only one label)
input_dict_test, output_dict_test = balance_label(input_dict_test, output_dict_test)

# shuffle the input (output shuffled in tfrecord accordingly with the key in
# convert_to_TFRecord)
input_dict_test, output_dict_test = shuffle_input_dict(
    input_dict_test, output_dict_test
)

"""
# turn train_dict into TFRecord (目前先放棄使用TFRecord)
file_dir = './docs/py_Train_flat.tfrecords'
convert_to_TFRecord(input_dict_train, output_dict_train, file_dir)
print("converting py_Train_flat.tfrecords")
"""

# save input_dict_train
file_path = os.path.dirname(os.path.realpath(__file__))
save_path = file_path + "/docs/" + "input_dict_train.pickle"
with open(save_path, "wb") as f:
    pickle.dump(input_dict_train, f)

# save output_dict_train
file_path = os.path.dirname(os.path.realpath(__file__))
save_path = file_path + "/docs/" + "output_dict_train.pickle"
with open(save_path, "wb") as f:
    pickle.dump(output_dict_train, f)

# save input_dict_test
file_path = os.path.dirname(os.path.realpath(__file__))
save_path = file_path + "/docs/" + "input_dict_test.pickle"
with open(save_path, "wb") as f:
    pickle.dump(input_dict_test, f)

# save output_dict_test
file_path = os.path.dirname(os.path.realpath(__file__))
save_path = file_path + "/docs/" + "output_dict_test.pickle"
with open(save_path, "wb") as f:
    pickle.dump(output_dict_test, f)

"""
#
#
#
#
#
# roll_conn #### (for CNN)
# turn key format from string into datetime
roll_conn_element_dict = {datetime.datetime.combine(fd.date_format(key),
                          datetime.time()): item for key, item in
                          roll_conn_dict.items()}
# for key, item in roll_conn_element_dict.items():
#     print(key)
#     print(item)


# turn into np.matrix
roll_conn_element_dict = {key: np.float32(np.array(item)) for key, item in
                          roll_conn_element_dict.items()}
# for key, item in roll_conn_dict.items():
#     print(key)
#     print(np.shape(item))


# turn into TFRecord
file_dir = './docs/py_Train_element.tfrecords'
# convert_to_TFRecord(roll_conn_element_dict, movement_dict, file_dir)
print("converting py_Train_element.tfrecords")
#
#
#
#
#
# roll_conn time_step #### (for CNN + RNN)

# turn into
roll_conn_elements_dict = conn_table_periods_converter(roll_conn_dict,
                                                       conns_for_one_element)

# turn into np.matrix
roll_conn_element_dict = {key: np.float32(np.array(item)) for key, item in
                          roll_conn_element_dict.items()}


# turn into TFRecord
file_dir = './docs/py_Train_elements.tfrecords'
convert_to_TFRecord(roll_conn_element_dict, movement_dict, file_dir)
print("converting py_Train_elements.tfrecords")


# count the elapsed time span, end time
elapsed_time = time.time() - start_time
print("the time span in data_TFREcotd_format ", elapsed_time)
print("===================")
"""
