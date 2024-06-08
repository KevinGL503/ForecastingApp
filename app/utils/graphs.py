import pickle 
import plotly.express as px
import requests
import pandas as pd
from dash import dash_table
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
BASE_URL = os.getenv('BASE_URL')

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
    curr = requests.get(f'{BASE_URL}/api/forecast/{region}')
    curr = pd.DataFrame(curr.json())
    curr.set_index('TS', inplace=True)
    prices = requests.get(f'{BASE_URL}/api/prices')
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

def get_table(type):
    """
    The function `get_table` retrieves data from a specified API endpoint, formats
    it into a DataFrame, and creates a Dash DataTable with specific styling and
    columns based on the type provided.
    
    :param type: The `type` parameter in the `get_table` function is used to specify
    the type of data to retrieve from the API. 
    :return: A Dash DataTable object displaying data from the specified type
    """
    df = requests.get(f'{BASE_URL}/api/{type.lower()}')
    df = pd.DataFrame(df.json())
    if type == 'Conditions': df = df[['TS', 'Load', 'Wind', 'Solar']]
    ts = df.pop('TS') 
    df.insert(0, 'TS', ts) 
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
    return prices