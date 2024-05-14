#%%
import pickle
import utils.get_curr_cond as util
import utils.graphs as gp
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash import Input, Output

dash.register_page(__name__)
fig = gp.get_graph('hbBusAvg')
layout = html.Div([
    html.H1('Daily SPPs (Actual vs Forecasted)',style={'padding':'30px'}
            ),
    dcc.Graph(figure=fig, id="Fuel-mix-graph", config={'displaylogo': False}),
])