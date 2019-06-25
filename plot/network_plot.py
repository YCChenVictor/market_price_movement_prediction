"""
The data acutally reflact the truth

should make it draw specific network, maybe the data to calculate connectedness
is too small
"""

import functions.f_connectedness as ff_conn
import functions.f_coef as ff_coef
import pickle
import os
import functions.f_network as ff_net
import functions.about_path as fap

# load volatility_dataframe
file_path = os.path.dirname(os.path.realpath(__file__))
parent_path = fap.f_parent_path(file_path, 1)
save_path = parent_path + '/full_predict_procedure_CNN_RNN' + '/docs/' + 'volatility.pickle'
with open(save_path, 'rb') as f:
    volatility_dataframe = pickle.load(f)
# print(volatility_dataframe)

# calculate estimated coefficients
coef = ff_coef.Coef(volatility_dataframe, 4)
coef.f_ols_coef()
ols_coef = coef.OLS_coef
# print(ols_coef)

# accuracy
accuracy = coef.accuracy
# print(accuracy)

# calculate estimated sigma given coef we want
# lag = coef.Lag[0]
# sx = coef.x
# sy = coef.y
ols_sigma = coef.OLS_sigma
# print(ols_sigma)

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
