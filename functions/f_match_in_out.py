def divide_df_into_batches(dataframe, n_steps):

    batches = []

    for i in range(len(dataframe)):
        batch = dataframe.iloc[i:(n_steps+i)]
        if len(batch) != n_steps:
            break
        batch = pd.DataFrame(batch)
        batches.append(batch)

    return batches


def last_date(dataframe):
    Dates = dataframe['Date']
    last_date = Dates.iloc[-1]
    return last_date


def match(input_list, label_list):

    in_out_dict = {}

    for dataframe in input_list:

        in_out = {}

        # add in into in_out
        in_out["in"] = dataframe

        # get the last date on a dataframe
        ldate = last_date(dataframe)

        # get the label matches the date
        label = label_list[(label_list['Date'] == ldate.strftime('%Y-%m-%d'))]

        # add out into in_out
        in_out["out"] = label

        # add into dict
        in_out_dict[ldate.strftime('%Y-%m-%d')] = in_out

    return in_out_dict