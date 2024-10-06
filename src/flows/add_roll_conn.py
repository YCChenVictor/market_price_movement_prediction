import os
import pickle
import functions.f_about_path as fap
import json
import functions.f_rolling_connectedness as f_roll
import time

# count the time span, start
start_time = time.time()


# load Prerequisite
file_path = os.path.dirname(os.path.realpath(__file__))
parent_path = fap.f_parent_path(file_path)
path = parent_path + "/docs/" + "Prerequisite.json"
with open(path) as f:
    prerequisite = json.load(f)


# varibales from prerequisite
target_folder = prerequisite["target_folder"]
predict_conns_periods = prerequisite["predict_conns_periods"]
maximum_lag = prerequisite["maximum_lag"]
periods_one_conn = prerequisite["periods_one_conn"]
start_dt = prerequisite["start_dt"]
end_dt = prerequisite["end_dt"]


# the number of data
# simple version for working with CWD
file_path = os.path.dirname(os.path.realpath(__file__))
parent_path = fap.f_parent_path(file_path, 0)
save_path = parent_path + "/docs/" + target_folder
# print(save_path)
n_instruments = sum([len(files) for r, d, files in os.walk(save_path)])


# delete .DS_store
if os.path.isfile(save_path + "/.DS_Store"):
    os.remove(save_path + "/.DS_Store")


# load volatility_dataframe
file_path = os.path.dirname(os.path.realpath(__file__))
save_path = file_path + "/docs/" + "volatility.pickle"
with open(save_path, "rb") as f:
    volatility_dataframe = pickle.load(f)
# print(volatility_dataframe)


# setup the rolling connectedness module
roll_conn = f_roll.Rolling_Connectedness(
    volatility_dataframe, maximum_lag, periods_one_conn, predict_conns_periods
)


# divide vol_dataframe into vol_dict
roll_conn.divide_vol_dataframe()


# load roll_conn dataset
file_path = os.path.dirname(os.path.realpath(__file__))
roll_conn_path = file_path + "/docs/" + "roll_conn.pickle"
with open(roll_conn_path, "rb") as f:
    roll_conn_dict = pickle.load(f)


# add the rolling_connectedness
file_path = os.path.dirname(os.path.realpath(__file__))
saving_folder = file_path + "/docs/"
roll_conn.add_connectedness_and_df(start_dt, end_dt, saving_folder)


# count the time span, end
elapsed_time = time.time() - start_time
print("the time span in calculating rolling connectedness:", elapsed_time)
print("===================")
