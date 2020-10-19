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
    FILE_EXT = '.png'
    
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
                          title={'text': fig_title, 'x':0.5, 'y':1})
        fig.show() if interactive else fig.show(Visualizer.FILE_EXT[1:])
        if save_info:
            fig.write_image('{path}/{name}{ext}'.format(
                path=save_info['path'], name=save_info['file_name'],
                ext=save_info['ext'] if 'ext' in save_info
                else Visualizer.FILE_EXT))
        
    
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
            title=color
        if not color_title:
            color_title=color
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