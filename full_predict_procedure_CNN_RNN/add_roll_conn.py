import os
import pickle
import functions.about_path as fap
import json
import functions.f_rolling_connectedness as f_roll
import time

# count the time span, start
start_time = time.time()

# load Prerequisite
file_path = os.path.dirname(os.path.realpath(__file__))
parent_path = fap.f_parent_path(file_path)
path = parent_path + '/docs/' + 'Prerequisite.json'
with open(path) as f:
    prerequisite = json.load(f)

# load volatility_dataframe
file_path = os.path.dirname(os.path.realpath(__file__))
save_path = file_path + '/docs/' + 'volatility.pickle'
with open(save_path, 'rb') as f:
    volatility_dataframe = pickle.load(f)
# print(volatility_dataframe)

# the number of data
# simple version for working with CWD
file_path = os.path.dirname(os.path.realpath(__file__))
parent_path = fap.f_parent_path(file_path, 0)
save_path = parent_path + '/docs/' + 'country_stock_csv'
# print(save_path)
n_stock = sum([len(files) for r, d, files in os.walk(save_path)])

# hyperparameters
maximum_lag = 30  # set the maximum lag periods for calculating connectedness
periods_one_conn = 35 * n_stock  # the more stock data, the more periods to
# //calculate the connectedness
predict_period = 1  # the number of prediction to future connectedness
# use 120 days (4 month) data to predict one day after connectedness. The
# //maximum lag is 30 days.

# setup the rolling connectedness module
roll_conn = (f_roll.
             Rolling_Connectedness(volatility_dataframe,
                                   maximum_lag,
                                   periods_one_conn,
                                   predict_period))

# divide vol_dataframe into vol_dict
roll_conn.divide_vol_dataframe()

# load roll_conn dataset
file_path = os.path.dirname(os.path.realpath(__file__))
roll_conn_path = file_path + '/docs/' + 'roll_conn.pickle'
with open(roll_conn_path, 'rb') as f:
    roll_conn_dict = pickle.load(f)

# setup the start date and end date
start_dt = prerequisite['start_dt']
end_dt = prerequisite['end_dt']

# add the rolling_connectedness
roll_conn.add_connectedness_and_df(roll_conn_dict, start_dt, end_dt)

# turn roll_conn_dict into df
roll_conn.turn_into_df()
print(roll_conn.df)

# save the dict to pickle so that I can add new element to the dict in the
# //future
file_path = os.path.dirname(os.path.realpath(__file__))
save_path = file_path + '/docs/' + 'roll_conn.pickle'
print(save_path)
with open(save_path, 'wb') as f:
    pickle.dump(roll_conn_dict, f)

# count the time span, end
elapsed_time = time.time() - start_time
print("the time span in calculating rolling connectedness:", elapsed_time)
print("===================")
