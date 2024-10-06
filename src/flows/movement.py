"""
Notice: The DS_store file will disrupt the process. delete it first.
"""

# import modules
import functions.f_movement as f_move
import os
import pickle
import time
import json

# import pandas as pd

# count the elapsed time span, start time
start_time = time.time()

# load Prerequisite
file_dir = os.path.dirname(os.path.abspath(__file__))
with open(file_dir + "/docs" + "/Prerequisite.json") as f:
    prerequisite = json.load(f)
# print(prerequisite)

# obtain start_date, end_date
end_dt = prerequisite["end_dt"]

# calculate movement
move = f_move.predict_movement(end_dt)
move.get_movements("label")
# print(move.dict_movement)

# get the movement dataframe
move.periods_of_movement()
movement_dataframe = move.dataframe
print(movement_dataframe)

# save the volatility_dataframe into pickle
file_path = os.path.dirname(os.path.realpath(__file__))
save_path = file_path + "/docs/" + "movement.pickle"
with open(save_path, "wb") as f:
    pickle.dump(movement_dataframe, f)

# count the elapsed time span, end time
elapsed_time = time.time() - start_time
print("the time span in calculating movement: ", elapsed_time)
print("===================")
