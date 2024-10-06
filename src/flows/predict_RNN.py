import pickle
import numpy as np
import os
from functions.f_train_model_RNN import get_model
import json

"""
以 2020/06/19 來看，應該是要預測為上漲，即為 1
"""

# The Prerequisite, n_instruments, tfrecords file ####
# import prerequiste
pre_path = "./docs/" + "Prerequisite.json"
with open(pre_path) as f:
    prerequisite = json.load(f)

# The variable from prerequsite
conns_for_one_element = prerequisite["conns_for_one_element"]
n_hidden_units = prerequisite["n_hidden_units"]

# get the number of price
target_folder = prerequisite["target_folder"]
file_path = os.path.dirname(os.path.realpath(__file__))
path = file_path + "/docs/" + target_folder
n_price = sum([len(files) for r, d, files in os.walk(path)])

# the number of elements in a connectedness table
n_table_elements = (n_price + 1) ** 2

# read the data for testing
with open("./docs/input_dict_test.pickle", "rb") as f:
    input_dict_test = pickle.load(f)
with open("./docs/output_dict_test.pickle", "rb") as f:
    output_dict_test = pickle.load(f)

# append output_dict_test
output_list_test = []
for key, item in output_dict_test.items():
    if item is not None:
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

# checkpoint
checkpoint_path = "./docs/checkpoint/cp.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)

# Loads the model
model = get_model(conns_for_one_element, n_table_elements, n_hidden_units)

# Loads the weights
model.load_weights(checkpoint_path)

# Re-evaluate the model
result = model.predict(X_test)
print(result)
