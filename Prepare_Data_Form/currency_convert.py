import os
import functions.about_path as fap
import pandas as pd

# import data
file_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = fap.f_parent_path(file_dir)
target_dir = parent_dir + '/docs' + '/csv_files_currency_investing'

# get all the names of the csv files
for root, dirs, files in os.walk(target_dir):
    csv_files = files
# print(csv_files)

# remove .DS_Store
csv_files.remove('.DS_Store')
# print(csv_files)

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
    dict_data[names[i]] = pd.read_csv(target_dir + "/" + csv_files[i],
                                      index_col=["Date"],
                                      parse_dates=['Date'])

# change the dates format
for key, item in dict_data.items():
    item.index = pd.to_datetime(item.index, format='%d-%m-%Y').strftime('%Y-%m-%d')
    print(key)
    item.to_csv(key, sep=',')
    print(item)

# read all the csv files and save it into dict_data
dict_data = {}  # the dictionary
for i in range(len(names)):
    dict_data[names[i]] = pd.read_csv(target_dir + "/" + csv_files[i],
                                      index_col=["Date"],
                                      parse_dates=['Date'])

# fill all the dates
for i in range(len(dict_data)):
    target = dict_data[names[i]]
    start_date = target.index[0]
    end_date = target.index[len(target.index)-1]
    if end_date < start_date:
        start_date = target.index[len(target.index)-1]
        end_date = target.index[0]
    dates = pd.date_range(start_date, end_date)
    dict_data[names[i]] = (target.reindex(dates))

for key, item in dict_data.items():
    print(item)
    item.to_csv(key, sep=',')

"""
# create column with row index
modifier = dict_data['USD_XDR']
"""
"""
# Concatenate the columns
for key, item in dict_data.items():
    dict_data[key] = pd.merge(item, modifier, left_index=True, right_index=True)
    # dict_data[key].to_csv(key)
    # print(dict_data[key])
"""

"""
# convert all the nan into zero
for key, item in dict_data.items():
    # print(key)
    dict_data[key] = item.fillna(0)
    # print(dict_data[key])

a = ['Close', 'Open', 'High', 'Low']

# convert to SDR base
for key, item in dict_data.items():
    print(key)
    for element in a:
        item[element] = item[element] * item['USD/XDR']
    dict_data[key] = item
    print(dict_data[key])
    item.to_csv(key, sep=',')
"""

"""
for key, item in dict_data.items():
    item.to_csv(key, sep=',')
"""
