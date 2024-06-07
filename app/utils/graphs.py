import pickle 
import plotly.express as px
import requests
import pandas as pd

def get_models(region):
    with open(f"./models/{region.upper()}_models.pkl", "rb") as f:
        print(f'got {region} model')
        linear = pickle.load(f)
        tree = pickle.load(f)
        forest = pickle.load(f)
        gb_model = pickle.load(f)
    return [linear, tree, forest, gb_model]


def get_graph(region):
    """
    The `get_graph` function generates a line plot comparing actual and forecasted
    daily SPPs using different predictive models.
    
    :param region: The `get_graph` function takes a `region` parameter as input.
    This parameter is used to retrieve current conditions data for the specified
    region. 
    :return: graph plot
    """
    curr = requests.get(f'http://localhost:5578/api/forecast/{region}')
    curr = pd.DataFrame(curr.json())
    curr.set_index('TS', inplace=True)
    prices = requests.get(f'http://localhost:5578/api/prices')
    prices = pd.DataFrame(prices.json())
    prices.set_index('TS', inplace=True)
    curr['Price'] =  prices[region.upper()]

    fig = px.line(curr, x=curr.index, y=['Price','GB'], 
                labels={'Price': 'Price ($)', 'TS': '', "value": 'Price'},
                title=f'Daily SPPs for {region}')
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