'''
The procedure:

1. read the name of csv file
2. delete all the data with exact same value to the last date of data
3. fill all the dates and interpolate it for nan values
'''

import os
import json
import pandas as pd
import pickle

# load Prerequisite
file_dir = os.path.dirname(os.path.abspath(__file__))
with open(file_dir + '/docs' + '/Prerequisite.json') as f:
    prerequisite = json.load(f)
# print(prerequisite)

# varibales from prerequisite
target_folder = prerequisite["target_folder"]
end_dt = prerequisite["end_dt"]

# get all the names of the csv files
file_dir = os.path.dirname(os.path.abspath(__file__))
path = file_dir + '/docs/' + target_folder
# print(path)
for root, dirs, files in os.walk(path):
    csv_files = files
# csv_files.remove('.DS_Store')

# get the names
names_list = []
names = csv_files
for name in names:
    name = name.replace('.csv', '')
    names_list.append(name)
names = names_list
# print(names)

# read all the csv files and save it into dict_data
dict_data = {}  # the dictionary
for i in range(len(names)):
    file = pd.read_csv(path + "/" + csv_files[i], index_col=["Date"],
                       parse_dates=["Date"])
    dict_data[names[i]] = file
# print(dict_data)


# delete all the repeated data, which means fake data
for key, item in dict_data.items():

    print("deleting the repeated data: ", key)
    # print('=============')

    df = item

    # delete the repeat data
    df = df.drop_duplicates()

# fill all the dates
for i in range(len(dict_data)):

    # specify the dataframe
    target = dict_data[names[i]]

    # get the start date of the df
    start_date = target.index[0]

    # get the end date of the df
    end_date = target.index[len(target.index)-1]

    # because the order of the price df may be reversed
    if end_date < start_date:
        start_date = target.index[len(target.index)-1]
        end_date = target.index[0]

    # fill all the dates
    x = pd.date_range(start_date, end_date)
    dict_data[names[i]] = (target.
                           reindex(pd.date_range(start_date, end_date),
                                   fill_value="NaN"))

# interploate (to create data)
for i in range(len(dict_data)):

    # obtain the target df
    target = dict_data[names[i]]

    # change the element type so that the data can be interpolate
    target = target.astype(float)

    # interpolate
    target = target.interpolate(method='linear', axis=0).ffill().bfill()

    # with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    #     print(target)

    # replace item with interpolated df
    dict_data[names[i]] = target

# select specified dates
for i in range(len(dict_data)):

    # specify df
    target = dict_data[names[i]]

    # make Date column
    target['Date'] = target.index.values

    # the index to get the rows with specified date
    mask = (target['Date'] <= end_dt)

    # get the df with specified date
    target = target.loc[mask]
    dict_data[names[i]] = target

print(dict_data)

# save the modified_price_df into pickle
file_path = os.path.dirname(os.path.realpath(__file__))
save_path = file_path + '/docs/' + 'modified_price_df.pickle'
with open(save_path, 'wb') as f:
    pickle.dump(dict_data, f)
