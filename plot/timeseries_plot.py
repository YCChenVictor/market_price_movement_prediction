import os
import pickle
import pandas as pd
import matplotlib
import functions.f_date as ffd
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates

# load data
file_path = os.path.dirname(os.path.realpath(__file__))
save_path = file_path + '/docs/' + 'roll_conn.pickle'
with open(save_path, 'rb') as f:
    roll_conn_dict = pickle.load(f)

# turn dict to df
result = pd.concat(roll_conn_dict)
result = result.reset_index().set_index('level_0').drop(['level_1'], axis=1)

# get the dates
dates = list(result.index)
start_dt = ffd.date_format(dates[0])
end_dt = ffd.date_format(dates[-1])
date_range = ffd.daterange(start_dt, end_dt)
date_list = []
for date in date_range:
    date_list.append(date)

# timeseries plot
x = np.array(date_list)
y = np.array(result['all->all'])

fig, ax = plt.subplots()
ax.plot(x, y)
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=5))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
fig.autofmt_xdate()
plt.show()
