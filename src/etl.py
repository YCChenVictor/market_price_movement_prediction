# Should deal with different timezone issue

import pandas as pd
from pathlib import Path

class ETL:
    def __init__(self, file_dir):
        self.file_dir = Path(file_dir)
        self.csv_files = list(self.file_dir.glob("*.csv"))
        self.names = [file.stem for file in self.csv_files]
        self.dict_data = {
            name: pd.read_csv(file, index_col="time", parse_dates=["time"]) for name, file in zip(self.names, self.csv_files)
        }
        self.start_at = None
        self.end_at = None

    def check_same_time_column(self):
        time_columns = [df.index for df in self.dict_data.values()]
        union_time_index = time_columns[0]

        for time_column in time_columns[1:]:
            union_time_index = union_time_index.union(time_column)

        for name, df in self.dict_data.items():
            self.dict_data[name] = df.reindex(union_time_index).interpolate(method='time')

        self.start_at = union_time_index[0]
        self.end_at = union_time_index[-1]

    def write_back_to_csv(self):
        for name, df in self.dict_data.items():
            file_path = self.file_dir / f"{name}.csv"
            df.to_csv(file_path)
            print(f"Written {name} to {file_path}")

    def process(self):
        self.check_same_time_column()
        self.write_back_to_csv()
