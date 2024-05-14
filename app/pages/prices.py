#%%
import utils.graphs as gp
import dash
from dash import dcc
from dash import html
from dash import Input, Output, State, callback

dash.register_page(__name__)
layout = html.Div([
    html.H1('Daily SPPs (Actual vs Forecasted)',style={'padding':'30px'}
            ),
    dcc.Dropdown(['hbBusAvg', 'hbNorth', 'hbWest'], ['hbBusAvg'], 
                 id='region_dropdown',
                 multi=True),
    html.Div(id='graph_container')
])

@callback(
    Output('graph_container', 'children'),
    [Input('region_dropdown', 'value')],
    [State('graph_container','children')]
)
def update_output(selection, curr_children):
    if not selection:
        return  # Return the existing list of children if no selection

    if not curr_children:
        curr_children = [] 
        act_children = []
    else: 
        # curr_children = [dcc.Graph(**child['props']) for child in curr_children]
        act_children = []
        for c in curr_children:
            if c['props']['id'][5::] in selection:
                act_children.append(dcc.Graph(**c['props']))
    # Create graphs for new selections only
    new_children = []
    for value in selection:
        # Check if this graph is already displayed
        if not any(child.id == f"graph-{value}" for child in act_children):
            fig = gp.get_graph(value)
            new_children.append(dcc.Graph(
                figure=fig,
                id=f"graph-{value}",
                config={'displaylogo': False}
            ))
        

    # Append new graph components to the existing children
    return act_children + new_children