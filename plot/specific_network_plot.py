"""
The data acutally reflact the truth
"""

import functions.f_connectedness as ff_conn
import functions.f_coef as ff_coef
import pickle
import os
import functions.f_network as ff_net
import functions.about_path as fap

# load volatility_dataframe
file_path = os.path.dirname(os.path.realpath(__file__))
save_path = file_path + '/docs/' + 'volatility.pickle'
with open(save_path, 'rb') as f:
    volatility_dataframe = pickle.load(f)

# the number of data
# simple version for working with CWD
file_path = os.path.dirname(os.path.realpath(__file__))
parent_path = fap.f_parent_path(file_path, 0)
save_path = parent_path + '/docs/' + 'csv_files_currency_investing'
n_stock = sum([len(files) for r, d, files in os.walk(save_path)])

# hyperparameters
periods_one_conn = 35 * n_stock  # the more stock data, the more periods to calculate the connectedness

# split volatility dataframe
net = ff_net.Specific_Network(volatility_dataframe, periods_one_conn)
net.divide_vol_dataframe()
vol_dict = net.vol_dict

# specify the volatility dataframe
date = "2008-07-04"
vol_df = vol_dict[date]

# calculate estimated coefficients
coef = ff_coef.Coef(vol_df, 30)
coef.f_ols_coef()
ols_coef = coef.OLS_coef

# accuracy
accuracy = coef.accuracy

# calculate estimated sigma given coef we want
# lag = coef.Lag[0]
# sx = coef.x
# sy = coef.y
ols_sigma = coef.OLS_sigma

# get the mode name
names = list(volatility_dataframe.columns.values)
names.remove('Date')
names.append("all")

# calculate connectedness
conn = ff_conn.Connectedness(ols_coef, ols_sigma)
conn.f_full_connectedness()
conn.rename_table(names)
table = conn.full_connectedness
# print(conn.table_restructure())

# draw the network
network = ff_net.Create_Network(table)
network.change_names(names)
network.create_network()
network.plot()
network.show_draw()
