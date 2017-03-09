import numpy as np
import plotly.plotly as py
import plotly.tools as tls

py.sign_in('bensondaled','iAkChsyTuhVV2sDLyBBj')

##

base_us = pd.read_pickle('base_us_table.pd')
data = base_us.copy()
data.loc[:,'value'] = data_means.values
data.loc[:,'code'] = data_means.index

##
data = [ dict(
        type='choropleth',
        autocolorscale = True,
        locations = data['code'],
        z = data['value'],
        locationmode = 'USA-states',
        text = data['text'],
        marker = dict(
            line = dict (
            color = 'rgb(255,255,255)',
            width = 2
            ) ),
        colorbar = dict(
            title = "sentiment score")
) ]


layout = dict(
        title = 'Rudimentary trump twitter sentiment analysis',
        geo = dict(
                scope='usa',
                projection=dict( type='albers usa' ),
                showlakes = False )
        )

fig = dict( data=data, layout=layout )
url = py.plot( fig, filename='example_map', show_link=False, auto_open=False)
##
