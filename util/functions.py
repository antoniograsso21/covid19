import datetime
import numpy as np
import pandas as pd
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go


class Functions:
    
    URL_ROOT = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-'
    FILE_NAME_ROOT = 'dpc-covid19-ita-'
    FILE_EXT = '.csv'
    
    def __init__(self):
        """
        TODO
        """
        pass
    
    @staticmethod
    def get_prev_days_date(d, days: int):
        """
        TODO
        """
        return d - datetime.timedelta(days=days)
    
    @staticmethod
    def get_previous_date(d):
        """
        TODO
        """
        return Functions.get_prev_days_date(d, 1)
    
    @staticmethod
    def get_url_root(level):
        """
        TODO
        """
        return Functions.URL_ROOT + level + '/' + Functions.FILE_NAME_ROOT + level
    
    @staticmethod
    def get_url_cum(level):
        """
        TODO
        """
        return Functions.get_url_root(level) + Functions.FILE_EXT
    
    @staticmethod
    def get_url_date(level, d):
        """
        Get csv file url according to specified date and level.
        
        :param d: Date
        :param level: Level of granularity. It can be one between
        'andamento-nazionale', 'regioni' or 'province'.
        
        :rtype: `str` url of the csv file
        """
        date_formatted = str(d).replace('-', '')
        return Functions.get_url_root(level) + '-' + date_formatted + Functions.FILE_EXT
    
    @staticmethod
    def replace_bt_with_taa(df):
        """
        Replace Trento and Bolzano province rows with aggregated Trentino-Alto Adige row
        """
        s_taa_right = df[df['codice_regione'] > 20][df.columns[6:-1]].sum()
        s_taa_left = pd.Series([df['data'][0], df['stato'][0], 4, 'Trentino-Alto Adige', 46.382635, 11.204676], df.columns[:6])
        row_taa = s_taa_left.append(s_taa_right)
        return df[df['codice_regione'] <= 20].append(row_taa, ignore_index=True)