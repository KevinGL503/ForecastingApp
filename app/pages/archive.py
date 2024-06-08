import dash
from dash import html, dash_table, dcc
import dash_bootstrap_components as dbc
from dash import Input, Output, State, callback
import app.utils.graphs as gp


dash.register_page(__name__)

layout = dbc.Container(
    [html.H2('Current data for prices and conditions'),
     dcc.Dropdown(['Prices','Conditions'], 
                    id='data_selector',
                    multi=True, style={'width':'50vw'}),
    html.Div([
        html.Div(id='table_container', 
                 style={
                'display': 'flex',
                'flex-direction': 'row', 
                'justify-content:':'center',
                'align-items':'center',
                'flex-wrap': 'wrap',
                'max-width':'100vw',
                'gap':'30px',
                'padding': '30px'
                })
    ])
    ], 
    style={'padding':'30px',
            'display': 'flex',
            'flex-direction': 'column', 
            'justify-content:':'center',
            'align-items':'center',
            'max-width':'100vw'
            }
    )

@callback(
    Output('table_container', 'children'),
    [Input('data_selector', 'value')],
    [State('table_container','children')]
)
def update_output(selection, curr_children):
    if not selection:
        return 

    new_children = []
    for value in selection:
        fig = gp.get_table(value)
        block = html.Div([html.H3(value), fig], id=f'table-{value}')
        new_children.append(block)
        
    return new_children