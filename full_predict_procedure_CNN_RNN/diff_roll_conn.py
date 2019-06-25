import os
import pickle
import pandas as pd
from functions.f_rolling_connectedness import diff_roll_conn
import functions.about_path as fap
import json
import functions.f_date as ffd

# import prerequisite
file_path = os.path.dirname(os.path.realpath(__file__))
parent_path = fap.f_parent_path(file_path)
path = parent_path + '/docs/' + 'Prerequisite.json'
with open(path) as f:
    prerequisite = json.load(f)
conns_for_diff = prerequisite["conns_for_diff"]

# import rolling connectedness dataframe
# import data
file_path = os.path.dirname(os.path.realpath(__file__))
roll_conn_path = file_path + '/docs/' + 'roll_conn.pickle'
with open(roll_conn_path, 'rb') as f:
    roll_conn = pickle.load(f)

# specify the chosen date
start_dt = prerequisite["start_dt"]
end_dt = prerequisite["end_dt"]
start_dt = ffd.date_format(start_dt)
end_dt = ffd.date_format(end_dt)
date_range = ffd.daterange(start_dt, end_dt)

date_list = []
for date in date_range:
    date_list.append(date.strftime('%Y-%m-%d'))
# print(date_list)

# choose the specified dates of rolling coonectedness
roll_conn = {date: roll_conn[date] for date in date_list}

# turn roll_conn_dict into df
result = pd.concat(roll_conn)
result = result.reset_index().set_index('level_0').drop(['level_1'], axis=1)
# print(result)

# divide and difference the rolling conncetedness
sliced_dict = diff_roll_conn(result, conns_for_diff)

# print part of the sliced_dict to show the result
print(list(sliced_dict.items())[-1])

# save the difference rolling connectedness
file_path = os.path.dirname(os.path.realpath(__file__))
save_path = file_path + '/docs/' + 'diff_roll_conn.pickle'
with open(save_path, 'wb') as f:
    pickle.dump(sliced_dict, f)
