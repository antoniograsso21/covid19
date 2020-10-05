import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


class Util:
    
    NATIONAL = 'N'
    REGION = 'R'
    PROVINCE = 'P'
    URL_ROOT = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-'
    FILE_NAME_ROOT = 'dpc-covid19-ita-'
    FILE_EXT = '.csv'
    
    def __init__(self):
        """
        TODO
        """
        pass
    
    @staticmethod
    def get_previous_date(d):
        """
        TODO
        """
        return d - datetime.timedelta(days=1)
    
    @staticmethod
    def get_url_date(d, level):
        """
        Get csv file url according to specified date and level.
        
        :param d: Date
        :param level: Level of granularity. It can be one between
        'andamento-nazionale', 'regioni' or 'province'.
        
        :rtype: `str` url of the csv file
        """
        date_formatted = str(d).replace('-', '')
        return Util.URL_ROOT + level + '/' + Util.FILE_NAME_ROOT + level + '-' + date_formatted + Util.FILE_EXT
    
    @staticmethod
    def replace_bt_with_taa(df):
        """
        Replace Trento and Bolzano province rows with aggregated Trentino-Alto Adige row
        """
        s_taa_right = df[df['codice_regione'] > 20][df.columns[6:-1]].sum()
        s_taa_left = pd.Series([df['data'][0], df['stato'][0], 4, 'Trentino-Alto Adige', 46.382635, 11.204676], df.columns[:6])
        row_taa = s_taa_left.append(s_taa_right)
        return df[df['codice_regione'] <= 20].append(row_taa, ignore_index=True)
    
    @staticmethod
    def choropleth_map(df, geojson, color, locations, featureidkey,
                       color_continuous_scale=px.colors.sequential.OrRd,
                       projection='mercator'):
        fig = px.choropleth(df,
                            geojson=geojson,
                            color=color,
                            locations=locations,
                            featureidkey=featureidkey,
                            color_continuous_scale=color_continuous_scale,
                            projection=projection)
        fig.update_geos(fitbounds='locations', visible=False)
        fig.update_layout(margin={'r': 0, 't': 0, 'l': 0, 'b': 0})
        return fig
        