import os
import functions.about_path as fap
import json

# fill the preresquite to run the program
preresquite = {"target_folder": "all",
               "start_dt": "2000-01-29",
               "end_dt": "2019-1-29",
               "conns_for_diff": 10,
               "conns_for_one_batch": 2,
               "predict_periods": 100}
"""
The start_dt and end_dt define the periods to calculate the predicted
connectedness

The conns_for_diff means how many periods to calculate the differenced
connectedness dataframe

The conns_for_one_batch defines how many periods in one batch
"""

file_path = os.path.dirname(os.path.realpath(__file__))
parent_path = fap.f_parent_path(file_path, 1)
move_path = parent_path + '/full_predict_procedure_CNN_RNN/' + 'docs/'+ 'Prerequisite.json'
with open(move_path, 'w') as outfile:
    json.dump(preresquite, outfile)

"""
# scrape finance data
print("scraping finance data")
import scrape_finance_data_yahoo
print("done ===")
"""

"""
# modify data
print("modifying data")
import load_and_modify_data
print("done ===")
"""

# calculate volatilities and movements (all periods)
print("calculating volatilities")
import volatility
print("done ===")

# draw network plot
print("drawing network plot")
import network_plot
print("done ===")
