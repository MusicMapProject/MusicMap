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
            [
                html.H1(
                    'MusicMap',
                    ),
            ],
        className = 'row'
    ),

    dcc.Graph(id='main_graph',
              figure = figure,
              className = 'two columns',
              style = {'margin-top': '5'}
              )
    ],
    className='three columns offset-by-two'
)

# Main graph -> indiviual graph
@app.callback(Output('main_graph', 'figure'),
              [Input('main_graph', 'clickData')])
def play_audio(main_graph_click):
    global first_click
    global player
    global cur_audio_name

    if first_click:
        first_click = False
        return figure

    audio_dir = "../data/our_audio/audio_parts/"

    if not main_graph_click:
        return figure

    chosen = [point['customdata'] for point in main_graph_click['points']]

    if len(chosen) > 1:
        print "Multiply clicks! Error!"
    else:
        filename, extension = os.path.splitext(chosen[0])
        audio_name = audio_dir + filename + ".wav"

        if cur_audio_name == audio_name:
            print "PAUSE"
            print player
            for i, p in enumerate(player):
                p.pause()
            player = []
            cur_audio_name = ""
            # player.pause()
            # player = None
        else:
            print "PLAY AUDIO, last", cur_audio_name
            print "NEW audio", audio_name
            if player:
                for i, p in enumerate(player):
                    p.pause()
                player = []
            audio = media.load(audio_name)
            try:
                print "APPEND"
                player.append(audio.play())
                # sleep(10)
                cur_audio_name = audio_name
            except Exception as e:
                print "I am here"
                print e

        # player.load(audio_dir + filename + ".wav")

    print len(chosen)
    print "CUR AUDIO ", cur_audio_name

    return figure


if __name__ == '__main__':
    print "OLOLOLO"
    global cur_audio_name
    global players
    global first_click
    first_click = True
    cur_audio_name = ""
    player = []
    app.server.run(host= '0.0.0.0', debug=True, threaded=True)
