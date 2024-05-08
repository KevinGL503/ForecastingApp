import pickle
from scripts.get_curr_cond import *
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash import Input, Output


app = dash.Dash(__name__)

with open("./models.pkl", "rb") as f:
    linear = pickle.load(f)
    tree = pickle.load(f)
    forest = pickle.load(f)
    gb_model = pickle.load(f)

app.layout = html.Div([
    html.H1('Daily SPPs (Actual vs Forecasted'),
    dcc.Graph(id="Fuel-mix-graph", config={'displaylogo': False}),
    dcc.Interval(
        id='interval-component',
        interval=17*60*1000, 
        n_intervals=0
    )
])


@app.callback(
    Output("Fuel-mix-graph", "figure"),
    Input('interval-component', 'n_intervals')
)
def update_graph(n):
    curr = get_curr_cond()
    curr.dropna(inplace=True)
    curr['Lin'] = linear.predict(curr[['Day', 'Hour', 'Wind', 'Solar', 'Load', 'Prev_Load', 'Net_Load', 'Total_Renew']])
    curr['Tree'] = tree.predict(curr[['Day', 'Hour', 'Wind', 'Solar', 'Load', 'Prev_Load', 'Net_Load', 'Total_Renew']])
    curr['Forest'] = forest.predict(curr[['Day', 'Hour', 'Wind', 'Solar', 'Load', 'Prev_Load', 'Net_Load', 'Total_Renew']])
    curr['GB'] = gb_model.predict(curr[['Day', 'Hour', 'Wind', 'Solar', 'Load', 'Prev_Load', 'Net_Load', 'Total_Renew']])

    fig = px.line(curr, x=curr.index, y=['Price','Forest'], 
                labels={'Price': 'Price ($)', 'TS': '', "value": 'Price'},
                title='Daily SPPs (Actual vs Forecasted)')
    fig.update_layout(legend_title_text='Models', hovermode="x unified")
    fig.update_traces(hovertemplate='$ %{y}')
    fig.update_layout(legend=dict(
        orientation="h",  
        yanchor="bottom",
        y=-0.25,
        xanchor="center",
        x=0.5
    ))

    return fig

if __name__ == '__main__':
    app.run_server(debug=True, host='euclid.local',port=5578)