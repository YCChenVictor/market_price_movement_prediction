"""
The procedure:

1. read the name of csv file
2. delete all the data with exact same value to the last date of data
3. fill all the dates and interpolate it for nan values
"""

import os
import json
import pandas as pd
import numpy as np
import pickle

# load Prerequisite
file_dir = os.path.dirname(os.path.abspath(__file__))
with open(file_dir + "/../../Prerequisite.json") as f:
    prerequisite = json.load(f)
target_folder = prerequisite["target_folder"]
start_time = prerequisite["start_time"]
end_time = prerequisite["end_time"]

# Get all the names of the csv files
file_dir = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(file_dir, "../../docs/market_prices/")
csv_files = []
for root, dirs, files in os.walk(path):
    csv_files.extend([file for file in files if file.endswith(".csv")])
names = [os.path.splitext(file)[0] for file in csv_files]

# read all the csv files and save it into dict_data
dict_data = {}  # the dictionary
for i in range(len(names)):
    file = pd.read_csv(
        path + "/" + csv_files[i], index_col=["time"], parse_dates=["time"]
    )
    dict_data[names[i]] = file
print(dict_data)

# delete all the repeated data, which means fake data
for key, item in dict_data.items():
    print("deleting the repeated data: ", key)
    df = item
    df = df.drop_duplicates()

# select specified dates
for i in range(len(dict_data)):
    target = dict_data[names[i]]
    np.datetime64(end_time)
    mask = target.index.values <= np.datetime64(end_time)
    target = target.loc[mask]
    dict_data[names[i]] = target

# save the modified_price_df into pickle
file_path = os.path.dirname(os.path.realpath(__file__))
docs_path = os.path.join(file_path, "../../docs")
if not os.path.exists(docs_path):
    os.makedirs(docs_path)
save_path = os.path.join(docs_path, "modified_price_df.pickle")
with open(save_path, "wb") as f:
    pickle.dump(dict_data, f)
