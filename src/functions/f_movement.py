import pandas as pd
import datetime
import os
import pickle
from functions.f_about_path import f_parent_path


def daterange(date1, date2):
    """
    :param date1: start date
    :param date2: end date
    :return: a list of date
    """
    for n in range(int((date2 - date1).days) + 1):
        yield date1 + datetime.timedelta(n)


def date_format(date):
    list_date = date.split("-")
    year, month, day = list_date[0], list_date[1], list_date[2]
    return datetime.date(int(year), int(month), int(day))


def movement_value(dataframe):

    # get the rownames
    rownames = dataframe.index
    # print(len(rownames))

    # list to save index
    index_list = []
    for index, row in dataframe.iterrows():

        Open = row["Open"]
        Close = row["Close"]

        movement = Close - Open

        """
        if Close > Open:
            movement = [[1, 0]]
        else:
            movement = [[0, 1]]
        """

        # list to save index
        index_list.append(movement)

    # turn the list into dataframe
    result = pd.DataFrame(index_list)
    result.index = rownames
    # print(result)

    # add new column of index to dataframe
    return result


def movement_label(dataframe):

    # get the rownames
    rownames = dataframe.index
    # print(len(rownames))

    # list to save index
    index_list = []
    for index, row in dataframe.iterrows():

        Open = row["Open"]
        Close = row["Close"]

        if Close > Open:
            movement = 1
        else:
            movement = 0

        # list to save index
        index_list.append(movement)

    # turn the list into dataframe
    result = pd.DataFrame(index_list)
    result.index = rownames
    # print(result)

    # add new column of index to dataframe
    return result


class predict_movement:

    def __init__(self, end_dt):

        # the required variables
        self.end_dt = end_dt

        # calculated movement
        self.dict_movement = None
        self.dataframe = None

    def get_movements(self, method):

        # import the stock price data
        file_path = os.path.dirname(os.path.realpath(__file__))
        parent_path = f_parent_path(file_path, 1)
        save_path = parent_path + "/docs/" + "modified_price_df.pickle"
        with open(save_path, "rb") as f:
            dict_data = pickle.load(f)

        # calculate movement (value or label)
        dict_movement = {}

        for data in dict_data:
            move_name = data + "_move"
            # print(movement(dict_data[data]))

            if method == "value":
                dict_movement[move_name] = movement_value(dict_data[data])
            elif method == "label":
                dict_movement[move_name] = movement_label(dict_data[data])
            else:
                print("The method can only be value or label")
        # print(dict_movement)

        self.dict_movement = dict_movement

    # obtain specify periods of volatility
    def periods_of_movement(self):

        start = date_format("1900-01-01")
        end = date_format(self.end_dt)

        list_date = []

        for dt in daterange(start, end):
            # print(dt)
            list_date.append(dt.strftime("%Y-%m-%d"))
            # print(type(dt.strftime("%Y-%m-%d")))

        # specify date here, create specified Date data
        dataframe_date = pd.DataFrame({"Date": list_date})
        dataframe_date.index = list_date

        # merge all the movements
        dict_movement = self.dict_movement
        result = dataframe_date
        for movement in dict_movement:
            # print(list(movement))
            movement_data = dict_movement[movement]
            movement_data.columns = [movement]
            # print(movement_data)
            result = result.merge(movement_data, left_index=True, right_index=True)
        # result = result.drop(columns=['Date'])

        self.dataframe = result
        # print(result)
