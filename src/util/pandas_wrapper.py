import pandas as pd


class DataFrameWrapper:
    """
    TODO
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def header_columns_lower(self):
        """
        Lower dataframe header columns
        """
        self.df.columns = [x.lower() for x in self.df.columns]

    def change_column_value(self, column_filter, value_filter, column_change,
                            value_change):
        """
        Change column value
        """
        self.df.loc[self.df[
            column_filter] == value_filter, [column_change]] = value_change
