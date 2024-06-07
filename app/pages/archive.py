import dash
from dash import html, dash_table, dcc
import requests
import pandas as pd
import dash_bootstrap_components as dbc


dash.register_page(__name__)
df = requests.get(f'http://localhost:5555/prices')
df = pd.DataFrame(df.json())
prices = dash_table.DataTable(
    data=df.to_dict('records'),
    columns=[{"name": i, "id": i} for i in df.columns],
    style_as_list_view=True,
    style_cell={'padding': '5px'},
    page_action='none',
    style_table={'height': '800px','overflowY': 'auto'},
    style_header={
        'backgroundColor': 'white',
        'fontWeight': 'bold',
        'textAlign': 'center'
    },
    )
df = requests.get(f'http://localhost:5555/conditions')
df = pd.DataFrame(df.json())
df = df[['TS', 'Load', 'Wind', 'Solar']]
conds = dash_table.DataTable(
    data=df.to_dict('records'),
    columns=[{"name": i, "id": i} for i in df.columns],
    style_as_list_view=True,
    style_cell={'padding': '5px'},
    page_action='none',
    style_table={'height': '800px','overflowY': 'auto'},
    style_header={
        'backgroundColor': 'white',
        'fontWeight': 'bold',
        'textAlign': 'center'
    },
    )

layout = dbc.Container([html.H3('This is the archive containing data for current day conditions and prices'),
    html.Div(
        [html.Div([
        html.H2('Prices'),
        prices],
        style={'padding':'30px',
            'display': 'flex',
            'flex-direction': 'column', 
            'justify-content:':'center',
            'align-items':'center',
            #   'column-gap': '100px',
            }),
        html.Div([
        html.H2('Conditions'),
        conds],
        style={'padding':'30px',
            'display': 'flex',
            'flex-direction': 'column', 
            'justify-content:':'center',
            'align-items':'center',
            #   'column-gap': '100px',
            }),
        ], 
        style={
            'display': 'flex',
            'flex-direction': 'row', 
            'justify-content:':'center',
            'align-items':'center',
            'flex-wrap': 'wrap',
            # 'flex-grow': '1'
            }
    )], 
    style={'padding':'30px',
            'display': 'flex',
            'flex-direction': 'column', 
            'justify-content:':'center',
            'align-items':'center',
            'max-width':'100vw'
            })