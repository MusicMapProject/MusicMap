import os
import pickle
import copy
import datetime as dt

import pandas as pd
from flask import Flask
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html


# In[]:
# Setup app
server = Flask(__name__)
server.secret_key = os.environ.get('secret_key', 'secret')

app = dash.Dash(__name__, server=server, url_base_pathname='/music_map/', csrf_protect=False)  # noqa: E501
app.css.append_css({'external_url': 'https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'})  # noqa: E501


# if 'DYNO' in os.environ:
#     app.scripts.append_script({
#         'external_url': 'https://cdn.rawgit.com/chriddyp/ca0d8f02a1659981a0ea7f013a378bbd/raw/e79f3f789517deec58f41251f7dbb6bee72c44ab/plotly_ga.js'  # noqa: E501
#     })


df = pd.read_csv("../data/our_audio/predictions")
print df.head()


# Create global chart template
# mapbox_access_token = 'pk.eyJ1IjoiamFja2x1byIsImEiOiJjajNlcnh3MzEwMHZtMzNueGw3NWw5ZXF5In0.fk8k06T96Ml9CLGgKmk81w'  # noqa: E501

layout = dict(
    images=[dict(
        # sizing="stretch",
        opacity = 1,
        layer = "below",
        xref = "x",
        yref = "y",
        sizex = 8,
        sizey = 8,
        source = "http://static.tumblr.com/c7iuapz/0mEnlqrs8/a4e096545ff6937dbf066981adf56ffe.media.700x700.jpg",
        y = 9,
        x = 1,
        sizing='contain'
      )],
    # autosize=True,
    height=850,
    width=850,
    font=dict(color='#CCCCCC'),
    titlefont=dict(color='#CCCCCC', size='14'),
    yaxis = {
          "zeroline": False,
          "title": "Valence",
          "range": [
            1,
            9
          ],
          "ticklen": 1,
          "showgrid": False
        },
    xaxis = {
          "zeroline": False,
          "title": "Arousal",
          "range": [
            1,
            9
          ],
          "ticklen": 1,
          "showgrid": False
    },
    # margin=dict(
    #     l=135,
    #     r=35,
    #     b=35,
    #     t=45
    # ),
    hovermode="closest",
    # plot_bgcolor="#191A1A",
    # paper_bgcolor="#020202",
    legend=dict(font=dict(size=10), orientation='h'),
    # title='MusicMap'
)


# In[]:
# Create app layout
app.layout = html.Div(children=
    [html.Div(
            [
                html.H1(
                    'MusicMap',
                    ),
            ],
        className = 'row'
    ),

    dcc.Graph(id='main_graph',
              figure =dict(
                        data = [dict(
                            type='scatter',
                            x=df['prediction_V'],
                            y=df['prediction_A'],
                            text=df['songnames'],
                            mode='markers',
                            marker=dict(
                                size=20,
                                opacity=0.8,
                                color="#ffba00"
                                )
                            )],
                        layout = layout
                        ),
              className = 'two columns',
              style = {'margin-top': '5'}
              )
    ],
    className='three columns offset-by-two'
)


if __name__ == '__main__':
    app.server.run(debug=True, threaded=True)
