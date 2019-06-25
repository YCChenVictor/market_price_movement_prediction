"""
I also need to do more research about forceatlas

Noe doing table restrcturing
"""

# import modules
import json
import functions.f_volatility as f_vol
import functions.f_coef as f_coef
import functions.f_connectedness as f_conn
# import functions.f_network as f_net
import os

# load Prerequisite
file_dir = os.path.dirname(os.path.abspath(__file__))
path = file_dir + '/docs/'
with open(path + 'Prerequisite.json') as f:
    prerequisite = json.load(f)

# varibales from prerequisite
target_folder = prerequisite["target_folder"]
start_dt = prerequisite["start_dt"]
end_dt = prerequisite["end_dt"]

# get all the names of the csv files
file_dir = os.path.dirname(os.path.abspath(__file__))
path = file_dir + '/docs/' + target_folder
for root, dirs, files in os.walk(path):
    csv_files = files

# specify all the names (this should be solve with json)
names = ["HK", "Japan", "Singapore", "China", "US", "UK", "Taiwan"]
if names is None:
    answer = input("whether to specify the names? y/N:")
    if answer == "y":
        print("please enter the list of the names matching the following csv" +
              "files")
        print(csv_files)
        names = input("input names:")
    else:
        names = csv_files

# calculate volatility dataframe
volatility = f_vol.volatility(names, csv_files, path, start_dt, end_dt)
volatility.price_data_to_volatility()
volatility.periods_of_volatility()
volatility_dataframe = volatility.dataframe

# save name of the dataframe
names = list(volatility_dataframe.columns.values)
names.remove('Date')
names.append("all")

# calculate estimated coefficients
coef = f_coef.Coef(volatility_dataframe, 20)
coef.f_ols_coef()
ols_coef = coef.OLS_coef

# accuracy
accuracy = coef.accuracy

# calculate estimated sigma given coef we want
# lag = coef.Lag[0]
# sx = coef.x
# sy = coef.y
ols_sigma = coef.OLS_sigma


# calculate connectedness
conn = f_conn.Connectedness(ols_coef, ols_sigma)
conn.f_full_connectedness()
conn.rename_table(names)
table = conn.full_connectedness
print(conn.table_restructure())

"""
# construct network plot
network = f_net.Create_Network(table)
network.change_names(names)
network.create_network()
network.plot()
network.show_draw()
"""
