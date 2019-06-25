import os
import pandas as pd

target_folder = 'csv_files_investing'
# find the data
file_dir = os.path.dirname(os.path.abspath(__file__))
path = file_dir + '/docs/' + target_folder
# print(path)
for root, dirs, files in os.walk(path):
    csv_files = files

# get the names
names_list = []
names = csv_files
for name in names:
    name = name.replace('.csv', '')
    names_list.append(name)
names = names_list

# read all the csv files and save it into dict_data
dict_data = {}  # the dictionary
for i in range(len(names)):
    file_name = csv_files[i]
    if file_name != '.DS_Store':
        dict_data[names[i]] = pd.read_csv(path + "/" + csv_files[i],
                                          index_col=["Date"],
                                          parse_dates=['Date'])

print(dict_data)
