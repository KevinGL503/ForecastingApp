""" This file contains functions to get the current day predicted conditions
    from ERCOT"""

import requests
import pandas as pd

def get_today_predicted_load():
    cond = requests.get("https://www.ercot.com/api/1/services/read/dashboards/combine-wind-solar.json")
    cond1 = cond.json()
    rows = []
    for conds in cond1['currentDay']['data'].values():
        this_row = {'TS':conds['timestamp'],
                    'wind':conds['stwpf'], 'solar':conds['stppf']}
        rows.append(this_row)
    df = pd.DataFrame(rows)
    df['TS'] = pd.to_datetime(df['TS'])

    return df