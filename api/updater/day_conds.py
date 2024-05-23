""" This file contains functions to get the current day predicted conditions
    from ERCOT"""

import requests
import pandas as pd

def get_today_predicted_fuel():
    """
    This function retrieves and processes data on wind and solar energy predictions
    for the current day.
    :return: dataframe with current day wind and solar predicted conditions
    """
    cond = requests.get("https://www.ercot.com/api/1/services/read/dashboards/combine-wind-solar.json")
    cond1 = cond.json()
    rows = []
    for conds in cond1['currentDay']['data'].values():
        this_row = {'TS':conds['timestamp'],
                    'Wind':conds['stwpf'], 'Solar':conds['stppf']}
        rows.append(this_row)
    df = pd.DataFrame(rows)
    df['TS'] = pd.to_datetime(df['TS'])

    return df

def get_today_predicted_load():
    """
    The function retrieves and processes the current day's predicted load data.
    :return: dataframe with current day wind and solar predicted conditions
    """

    cond = requests.get("https://www.ercot.com/api/1/services/read/dashboards/system-wide-demand.json")
    load = cond.json()
    rows = []
    for l in load['currentDay']['data']:
        this_row = {'TS':l['timestamp'],
                    'Load':l['currentLoadForecast']}
        rows.append(this_row)
    df = pd.DataFrame(rows)
    df['TS'] = pd.to_datetime(df['TS'])

    return df


def get_today_cond():
    """
    This function processes predicted fuel data and load data for today, resamples
    it to 15-minute intervals, and does the feature eng. needed for forecasting models.
    :return: dataframe with data needed for forecasts
    """

    df = get_today_predicted_fuel()
    load = get_today_predicted_load()
    df.set_index('TS', inplace=True)
    load.set_index('TS', inplace=True)
    df = df.resample('15min').asfreq().interpolate(method='linear')
    load = load.resample('15min').asfreq().interpolate(method='linear')

    df['Load'] = load['Load']
    df['Day'] = df.index.weekday
    df['Hour'] = df.index.hour
    df['Prev_Load'] = df['Load'].shift(1)
    df['Net_Load'] = df['Load'] - df['Wind'] - df['Solar']
    df['Total_Renew'] = df['Wind'] + df['Solar']
    df['Month'] = df.index.month
    df.bfill(inplace=True)
    return df[['Day', 'Hour', 'Wind', 'Solar', 'Load', 'Prev_Load', 'Net_Load', 'Total_Renew', 'Month']]
