""" This file contains functions to create forecasts """
import updater.day_conds as dc
from updater.db_helpers import DB
import pandas as pd
import pickle
import plotly.express as px

def get_models(region):
    with open(f"./models/{region.upper()}_models.pkl", "rb") as f:
        linear = pickle.load(f)
        tree = pickle.load(f)
        forest = pickle.load(f)
        gb_model = pickle.load(f)
    return [linear, tree, forest, gb_model]

def create_current_forecasts():
    """
    The function creates current forecasts for different regions using machine
    learning models and stores the results in the database as tables named `REGION_forecasts`.
    """
    db = DB()
    df = db.get_stored_curr_cond()
    hbs = ['HBHUBAVG', 'HBBUSAVG', 'HBSOUTH', 'HBWEST', 'HBNORTH', \
                    'HBHOUSTON', 'HBPAN']
    for hb in hbs:
        linear, tree, forest, gb_model = get_models(hb)
        curr = df.copy()
        cols = ['Day', 'Hour', 'Wind', 'Solar', 'Load', 'Prev_Load', 'Net_Load', \
                'Total_Renew', 'Month']
        curr['Lin'] = linear.predict(curr[cols])
        curr['Tree'] = tree.predict(curr[cols])
        curr['Forest'] = forest.predict(curr[cols])
        curr['GB'] = gb_model.predict(curr[cols])

        curr.drop(columns=cols).to_sql(f'{hb}_forecasts', db.con, if_exists='replace', \
                                index=True, index_label='TS')