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
import os
import pyglet.media as media
from time import sleep
# In[]:
# Setup app
server = Flask(__name__)
server.secret_key = os.environ.get('secret_key', 'secret')

app = dash.Dash(__name__, server=server, url_base_pathname='/music_map/', csrf_protect=False)  # noqa: E501
app.css.append_css({'external_url': 'https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'})  # noqa: E501
app.css.append_css({'external_url': 'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta/css/bootstrap.min.css'})  # noqa: E501
app.scripts.append_script({
    "external_url": "/static/framework/js/SSUhtml5Audio.js"
})

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
    #     t=45ntrols.
    # ),
    hovermode="closest",
    # plot_bgcolor="#191A1A",
    # paper_bgcolor="#020202",
    legend=dict(font=dict(size=10), orientation='h'),
    # title='MusicMap'
)

figure = dict(
            data = [dict(
                type='scatter',
                x=df['prediction_V'],
                y=df['prediction_A'],
                text=df['songnames'],
                customdata = df['songnames'],
                mode='markers',
                marker=dict(
                    size=30,
                    opacity=0.8,
                    color="#ffba00"
                    )
                )],
            layout = layout
            )


app.layout = html.Div(children=
    [html.Div(
        html.H1(
            'Music Map',
            style = {'margin-top': '15', "font-size":"50px"},
            className='col-md-auto'
            ),
        # className='row'
        className="row justify-content-center"
    ),

    html.Div(
        [
        # className='medium-5 columns offset-by-two'
        html.Div(
            dcc.Graph(id='main_graph',
                      figure = figure,

                      # style = {'margin-top': '5'}
                      ),
            className='col-md-auto'
        ),
        html.Div(
            children = [html.Audio(id='player',
                       # src="",
                       src="/static/Imagine Dragons - Thunder_3.wav",
                       style = {"margin-top":"100", "width":"500"},
                       controls="controls",
                       contextMenu="trololo",
                       # autoPlay = "false",
                       contentEditable="contentEditable",
                       title="kekekekekke",
                       draggable='draggable')],
            className='col-md-4',
            id = 'players'
        )
        ],

        className="row justify-content-center"
    )]
)

@app.callback(Output('players', 'children'),
              [Input('main_graph', 'clickData')],
               [State('players', 'children')])
def play_audio(main_graph_click, cur_players):
    audio_dir = "/static/audio_parts/"
    # print cur_players
    cur_audio_name = cur_players[0]["props"]["contextMenu"]

    if not main_graph_click:
        return cur_players

    chosen = [point['customdata'] for point in main_graph_click['points']]

    if len(chosen) > 1:
        print "Multiply clicks! Error!"
    else:
        filename, extension = os.path.splitext(chosen[0])
        audio_name = audio_dir + filename + ".wav"

        if cur_audio_name == audio_name:
            cur_players[0]["props"]["src"] = ""
            cur_players[0]["props"]["contextMenu"] = ""
        else:
            cur_players[0]["props"]["src"] = audio_name
            cur_players[0]["props"]["contextMenu"] = audio_name
            cur_players[0]["props"]["autoPlay"] = "autoPlay"


    return cur_players


if __name__ == '__main__':
    print "OLOLOLO"
    global cur_audio_name
    global players
    global first_click
    first_click = True
    cur_audio_name = ""
    player = []
    app.server.run(host= '0.0.0.0', debug=True, threaded=True)
