import utils.get_curr_cond as cc
import pickle 
import plotly.express as px

def get_models():
    with open("./models/models.pkl", "rb") as f:
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
    
    linear, tree, forest, gb_model = get_models()
    curr = cc.get_curr_cond(region)
    curr.dropna(inplace=True)
    curr['Lin'] = linear.predict(curr[['Day', 'Hour', 'Wind', 'Solar', 'Load', 'Prev_Load', 'Net_Load', 'Total_Renew']])
    curr['Tree'] = tree.predict(curr[['Day', 'Hour', 'Wind', 'Solar', 'Load', 'Prev_Load', 'Net_Load', 'Total_Renew']])
    curr['Forest'] = forest.predict(curr[['Day', 'Hour', 'Wind', 'Solar', 'Load', 'Prev_Load', 'Net_Load', 'Total_Renew']])
    curr['GB'] = gb_model.predict(curr[['Day', 'Hour', 'Wind', 'Solar', 'Load', 'Prev_Load', 'Net_Load', 'Total_Renew']])

    fig = px.line(curr, x=curr.index, y=['Price','GB'], 
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