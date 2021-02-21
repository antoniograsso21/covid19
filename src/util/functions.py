import json
import datetime
import requests
import numpy as np
import pandas as pd
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go


class Functions:

    URL_PC_COVID_ROOT = (
        'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-')
    FILE_NAME_PC_COVID_ROOT = 'dpc-covid19-ita-'

    URL_AGENAS_ROOT = 'https://www.agenas.gov.it'
    URL_COVID = 'covid19/web/index.php'
    URL_ICU_PAGE_PARAMS = 'r=site%2Ftab2'
    URL_ICU_JSON_PARAMS = 'r=json%2Ftab2'
    URL_ICU_PAGE = f'{URL_AGENAS_ROOT}/{URL_COVID}?{URL_ICU_PAGE_PARAMS}'
    URL_ICU_JSON = f'{URL_AGENAS_ROOT}/{URL_COVID}?{URL_ICU_JSON_PARAMS}'

    HEADERS_MOZILLA = {"User-Agent": "Mozilla/5.0"}

    URL_VACCINE_ROOT = (
        'https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/'
        'master/dati')

    # TODO: maybe remove full stop
    FILE_EXT = '.csv'

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
    def get_url_pc_covid(level):
        """
        TODO
        """
        return (
            f'{Functions.URL_PC_COVID_ROOT}{level}/'
            f'{Functions.FILE_NAME_PC_COVID_ROOT}{level}')

    @staticmethod
    def get_url_cum(level):
        """
        TODO
        """
        return f'{Functions.get_url_pc_covid(level)}{Functions.FILE_EXT}'

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
        return (
            f'{Functions.get_url_pc_covid(level)}-{date_formatted}'
            f'{Functions.FILE_EXT}')

    @staticmethod
    def replace_bt_with_taa(df):
        """
        Replace Trento and Bolzano province rows with aggregated Trentino-Alto
        Adige row.
        """
        s_taa_right = df[df['codice_regione'] > 20][df.columns[3:]] \
            .sum().astype(int)
        s_taa_left = pd.Series([df['data'].iloc[0], 4, 'Trentino-Alto Adige'],
                               df.columns[:3])
        row_taa = s_taa_left.append(s_taa_right)
        df_result = df[df['codice_regione'] <= 20] \
            .append(row_taa, ignore_index=True)
        return df_result

    @staticmethod
    def icu_data():
        """
        Return Italy icu updated data

        https://www.agenas.gov.it/covid19/web/index.php?r=site%2Ftab2
        """
        res_icu_page = requests.get(
            url=Functions.URL_ICU_PAGE, headers=Functions.HEADERS_MOZILLA)
        html_content = res_icu_page.content.decode('UTF-8')
        html_parse_start = 'ajax('
        html_parse_end = "dataType"
        icu_json_params = ("".join(
            html_content.split(html_parse_start)[1]
            .split(html_parse_end)[0].split())[:-1]).replace(",", ", ")
        username_key, password_key = "username", "password"
        headers_key = "headers"
        username = (icu_json_params.split(f'{username_key}:')[1]
                    .split(',')[0].replace("'", ''))
        password = (icu_json_params.split(f'{password_key}:')[1]
                    .split(',')[0].replace("'", ''))
        headers = eval(icu_json_params.split(f'{headers_key}:')[1])
        headers['User-Agent'] = Functions.HEADERS_MOZILLA['User-Agent']
        res_icu_json = requests.get(
            url=Functions.URL_ICU_JSON, auth=(username, password),
            headers=headers).content.decode('UTF-8')
        # Mapping json attributes - table attributes
        key_mapping = {
            'dato1': 'ricoverati_area_non_critica',
            'dato2': 'posti_letto_area_non_critica',
            'dato3': 'ricoverati_terapia_intensiva',
            'dato4': 'posti_letto_terapia_intensiva',
            'dato5': 'posti_letto_terapia_intensiva_attivabili'}
        for k in key_mapping:
            res_icu_json = res_icu_json.replace(k, key_mapping[k])
        icu_data = json.loads(res_icu_json)
        return icu_data

    @staticmethod
    def url_vaccine(file_name: str):
        return f'{Functions.URL_VACCINE_ROOT}/{file_name}{Functions.FILE_EXT}'
