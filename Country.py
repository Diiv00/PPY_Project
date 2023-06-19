import pandas as pd
from pathlib import Path


# class representing single instance of data for a country
class Country:
    def __init__(self, file_path):
        # name of the country extracted from path
        self.name = Path(file_path).stem
        print('Loading:', self.name)

        # data is a dataframe representing data for this country
        self.data = pd.read_csv(file_path, header=0, parse_dates=['utc_timestamp'], sep=',')

        # very simple data cleaning
        self.data.drop_duplicates()
        self.data.dropna(inplace=True)

        # set date to be the index instead of default one
        self.data.set_index('utc_timestamp', inplace=True)

    # return pandas dataframe with data about this country
    def get_data(self):
        return self.data

    # return minimal year from dataframe of this country
    def get_min_year(self):
        min_date = self.data.idxmin().iloc[0]
        return min_date.year

    # return maximal year from dataframe of this country
    def get_max_year(self):
        max_date = self.data.idxmax().iloc[0]
        return max_date.year

    # return name of this country
    def get_name(self):
        return self.name
