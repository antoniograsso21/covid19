import datetime
import numpy as np
import pandas as pd
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go


class Visualizer:

    COLORS = {'seq': px.colors.sequential, 
              'div': px.colors.diverging,
              'cyc': px.colors.cyclical}
    FILE_EXT = 'png'

    @staticmethod
    def choropleth_go(df,
                      locations,
                      geojson,
                      featureidkey,
                      color,
                      colorscale_type='seq',
                      colorscale_color='Reds',
                      reversescale=False,
                      zmid=None,
                      zmin=None,
                      zmax=None,
                      colorbar_title='',
                      fig_title='',
                      save_info=None,
                      interactive=False,
                      projection='mercator'):
        """
        TODO
        """
        colorscale = getattr(Visualizer.COLORS[colorscale_type], colorscale_color)

        fig = go.Figure(
            data=go.Choropleth(
                geojson=geojson,
                locations=df[locations], 
                z=df[color],
                featureidkey=featureidkey,
                colorscale=colorscale,
                reversescale=reversescale,
                zmid=zmid,
                zmin=zmin,
                zmax=zmax,
                colorbar_title=colorbar_title
            ))
        fig.update_geos(fitbounds='locations',
                        visible=False,
                        projection={'type': projection})
        fig.update_layout(margin={'r': 0, 't': 0, 'l': 0, 'b': 0},
                          title={'text': fig_title, 'x': 0.5, 'y': 1})
        fig.show() if interactive else fig.show(Visualizer.FILE_EXT)
        if save_info:
            path_save = '{path}/{name}.{ext}'.format(
                path=save_info['path'], name=save_info['file_name'],
                ext=save_info['ext'] if 'ext' in save_info
                else Visualizer.FILE_EXT)
            if 'ext' in save_info and save_info['ext'] == 'html':
                fig.write_html(path_save)
            else:
                fig.write_image(path_save)

    @staticmethod
    def choropleth_px(df,
                      geojson,
                      color,
                      locations,
                      featureidkey,
                      color_continuous_scale=px.colors.sequential.OrRd,
                      color_continuous_midpoint=None,
                      reversescale=False,
                      title=None,
                      color_title=None,
                      projection='mercator',
                      interactive=False):
        """
        TODO
        """
        if not title:
            title = color
        if not color_title:
            color_title = color
        fig = px.choropleth(
            df,
            geojson=geojson,
            color=color,
            locations=locations,
            featureidkey=featureidkey,
            color_continuous_scale=color_continuous_scale,
            color_continuous_midpoint=color_continuous_midpoint,
            projection=projection)
        fig.update_geos(fitbounds='locations', visible=False)
        fig.update_layout(margin={'r': 0, 't': 0, 'l': 0, 'b': 0},
                          coloraxis={'colorbar':{'title':color_title},
                                     'reversescale': reversescale},
                          title={'text': title, 'x':0.5, 'y':1})
        fig.show() if interactive else fig.show('png')
        return fig

    @staticmethod
    def colors_from_values(values, palette_name):
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

    @staticmethod
    def plot_hist_from_values(df, x_values, y_values, x_label, y_label,
                              x_ticks=None, y_ticks=None,
                              color='YlOrRd', reversescale=False, labels_font=14, save_info=None,
                              fig_size=(12, 8)):
        """
        TODO
        """
        sns.set(rc={'figure.figsize':fig_size})
        # sns.set_style('ticks')
        if reversescale:
            color += '_r'
        # color = 'RdYlGn_r'  # reversed palette
        palette = Visualizer.colors_from_values(df[y_values], color)
        g = sns.barplot(x=x_values, y=y_values, palette=palette, data=df);
        # g = sns.barplot(x='data', y='np_su_nt', color='red', data=df_n);
        # TODO: parametric rotation
        x_ticks_labels = x_ticks if x_ticks is not None else g.get_xticks()
        y_ticks_labels = y_ticks if y_ticks is not None else g.get_yticks()
        # Set axes ticks
        label_format = '{:.0f}'
        g.set_yticks(g.get_yticks().tolist())
        g.set_xticklabels(labels=x_ticks_labels, fontsize=labels_font - 1, rotation=90)
        g.set_yticklabels(labels=[label_format.format(x) for x in g.get_yticks().tolist()], fontsize=labels_font - 1)
        # Set axes labels
        g.set_xlabel(x_label, fontsize=labels_font)
        g.set_ylabel(y_label, fontsize=labels_font)
        if save_info:
            g.get_figure().savefig('{path}/{name}.{ext}'.format(
                path=save_info['path'], name=save_info['file_name'],
                ext=save_info['ext'] if 'ext' in save_info
                else Visualizer.FILE_EXT), bbox_inches='tight')


class ChoroplethMap:

    COLORS = {'seq': px.colors.sequential,
              'div': px.colors.diverging,
              'cyc': px.colors.cyclical}

    def __init__(self, df, geo_map, geo_col: str, geo_prop: str,
                 fig_prop, projection='mercator', file_ext: str = 'png'):
        self.df = df
        self.geo_map = geo_map
        self.geo_col = geo_col
        self.geo_prop = geo_prop
        self.fig_prop = fig_prop
        self.projection = projection
        self._file_ext = file_ext

    @property
    def file_ext(self):
        return self._file_ext

    def draw_map(self, col: str,
                 color: dict = {'type': 'seq', 'scale': 'Reds'},
                 reversescale: bool = False, zmin: int = None,
                 zmid: int = None, zmax: int = None,
                 interactive: bool = False):

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
        fig.show() if interactive else fig.show(self.file_ext)

        return fig

    def save(self, fig, col: str):
        path_out = '{path_root}/{name}.{ext}'.format(
            path_root=self.fig_prop['path_root'],
            name=self.fig_prop[col]['file_name'],
            ext=self.file_ext)
        if self.file_ext == 'html':
            fig.write_html(path_out)
        else:
            fig.write_image(path_out)
