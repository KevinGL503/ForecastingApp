""" This file contains functions to create forecasts """
import day_conds as dc
from db_helpers import DB
import pandas as pd
import pickle
import plotly.express as px

def get_models():
    with open("./models/models.pkl", "rb") as f:
        linear = pickle.load(f)
        tree = pickle.load(f)
        forest = pickle.load(f)
        gb_model = pickle.load(f)
    return [linear, tree, forest, gb_model]


def create_current_forecasts():
    db = DB()
    df = db.get_stored_curr_cond()
    linear, tree, forest, gb_model = get_models()
    curr = df.copy()
    cols = ['Day', 'Hour', 'Wind', 'Solar', 'Load', 'Prev_Load', 'Net_Load', \
            'Total_Renew', 'Month']
    curr['Lin'] = linear.predict(curr[cols])
    curr['Tree'] = tree.predict(curr[cols])
    curr['Forest'] = forest.predict(curr[cols])
    curr['GB'] = gb_model.predict(curr[cols])

    curr.drop(columns=cols).to_sql('forecasts', db.con, if_exists='replace', \
                            index=True, index_label='TS')


if __name__ == '__main__':
    db = DB()
    db.update_curr_prices()
    db.update_curr_cond()
    create_current_forecasts()
    