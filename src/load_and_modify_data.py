# Should deal with different timezone issue

import pandas as pd
from pathlib import Path


def load_and_process_market_data(file_dir):
    file_dir = Path(file_dir)
    csv_files = list(file_dir.glob("*.csv"))
    names = [file.stem for file in csv_files]
    dict_data = {
        name: pd.read_csv(file, index_col="time", parse_dates=["time"])
        for name, file in zip(names, csv_files)
    }

    return dict_data
