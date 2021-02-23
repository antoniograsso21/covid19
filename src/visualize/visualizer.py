import datetime
import numpy as np
import pandas as pd
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go


class ChoroplethMap:
    """
    Wraps a Pandas dataframe and a Geojson map for dataframe columns
    visualization on a choropleth map.

    :param df: dataframe with numerical columns
    :param geo_map: geojson map
    :param geo_col: dataframe column to locate geojson map areas
    :param geo_prop: geojson file property to detect dataframe rows
    :param fig_prop: figure property
    :param projection: type of map projection
    """
    COLORS = {'seq': px.colors.sequential,
              'div': px.colors.diverging,
              'cyc': px.colors.cyclical}

    def __init__(self,
                 df,
                 geo_map,
                 geo_col: str,
                 geo_prop: str,
                 fig_prop: dict,
                 projection='mercator'):
        self.df = df
        self.geo_map = geo_map
        self.geo_col = geo_col
        self.geo_prop = geo_prop
        self.fig_prop = fig_prop
        self.projection = projection

    def draw_map(self,
                 col: str,
                 color: dict = {'type': 'seq', 'scale': 'Reds'},
                 reversescale: bool = False,
                 zmin: int = None,
                 zmid: int = None,
                 zmax: int = None,
                 interactive: bool = False):
        """
        :param col: column to visualize on the map
        TODO
        :param color: TODO
        :param reversescale:
        :param zmin:
        :param zmid:
        :param zmax:
        :param interactive:
        """
        colorscale = getattr(ChoroplethMap.COLORS[color['type']],
                             color['scale'])
        fig_title, colorbar_title = self.fig_prop['title'], \
            self.fig_prop[col]['colorbar_title']

        fig = go.Figure(
            data=go.Choropleth(
                geojson=self.geo_map,
                locations=self.df[self.geo_col],
                z=self.df[col],
                featureidkey=self.geo_prop,
                colorscale=colorscale,
                reversescale=reversescale,
                zmid=zmid,
                zmin=zmin,
                zmax=zmax,
                colorbar_title=colorbar_title
            ))

        fig.update_geos(fitbounds='locations',
                        visible=False,
                        projection={'type': self.projection})

        fig.update_layout(margin={'r': 0, 't': 0, 'l': 0, 'b': 0},
                          title={'text': fig_title, 'x': 0.5, 'y': 1})

        # Display either static or interactive map
        fig.show() if interactive else fig.show('png')

        return fig

    def save(self, fig, col: str, file_ext: str = 'png'):
        """
        TODO
        :param fig: choropleth figure
        :param col: column whose map is to be saved
        :param file_ext: image extension
        """
        path_out = '{path_root}/{name}.{ext}'.format(
            path_root=self.fig_prop['path_root'],
            name=self.fig_prop[col]['file_name'],
            ext=file_ext)
        if file_ext == 'html':
            fig.write_html(path_out)
        else:
            fig.write_image(path_out)


class BarPlot:
    """
    TODO
    """

    def __init__(self,
                 df,
                 x_col: str,
                 graph_prop: dict):
        self._df = df
        self._x_col = x_col
        self._graph_prop = graph_prop

    @property
    def df(self):
        return self._df

    @df.setter
    def df(self, value):
        self._df = value

    @property
    def x_col(self):
        return self._x_col

    @property
    def graph_prop(self):
        return self._graph_prop

    @graph_prop.setter
    def graph_prop(self, value):
        self._graph_prop = value

    def _fig_size(self):
        num_rows = len(self.df)
        fig_size = (7.5, 6)
        if 10 < num_rows < 35:
            fig_size = (12, 8)
        elif num_rows > 35:
            fig_size = (15, 8)
        return fig_size

    def _colors_from_values(self, values, palette_name):
        """
        TODO
        """
        # normalize the values to range [0, 1]
        normalized = (values - min(values)) / (max(values) - min(values))
        # convert to indices
        indices = np.round(normalized * (len(values) - 1)).astype(np.int32)
        # use the indices to get the colors
        palette = sns.color_palette(palette_name, len(values))
        return np.array(palette).take(indices, axis=0)

    def draw_bar_plot(self,
                      y_col: str,
                      color='YlOrRd',
                      reversescale=False):
        """
        TODO
        """
        fig_size = self._fig_size()
        sns.set(rc={'figure.figsize': fig_size})
        # sns.set_style('ticks')
        if reversescale:
            color += '_r'
        # color = 'RdYlGn_r'  # reversed palette
        palette = self._colors_from_values(self.df[y_col], color)
        g = sns.barplot(x=self.x_col, y=y_col, palette=palette,
                        data=self.df);
        # g = sns.barplot(x='data', y='np_su_nt', color='red', data=df_n);
        # TODO: parametric rotation
        x_col_prop = self.graph_prop[self.x_col]
        y_col_prop = self.graph_prop[y_col]

        x_ticks_labels = self.df[self.x_col].apply(x_col_prop['ticks']) \
            if 'ticks' in x_col_prop else g.get_xticks()
        y_ticks_labels = self.df[y_col].apply(y_col_prop['ticks']) \
            if 'ticks' in y_col_prop else g.get_yticks()
        label_format = '{:.0f}'
        label_font = self.graph_prop['label_font']

        # TODO: check
        g.set_xticklabels(
            labels=x_ticks_labels, fontsize=label_font - 1, rotation=90)

        g.set_yticks(g.get_yticks().tolist())
        g.set_yticklabels(
            labels=[label_format.format(x) for x in g.get_yticks().tolist()],
            fontsize=label_font - 1)
        # Set axes labels
        g.set_xlabel(self.graph_prop[self.x_col]['label'],
                     fontsize=label_font)
        g.set_ylabel(self.graph_prop[y_col]['label'], fontsize=label_font)
        fig = g.get_figure()
        return fig

    def save(self, fig, y_col: str, file_ext: str = 'png'):
        path_out = '{path_root}/{name}.{ext}'.format(
            path_root=self.graph_prop['path_root'],
            name=self.graph_prop[y_col]['file_name'],
            ext=file_ext)
        fig.savefig(path_out, bbox_inches='tight')
