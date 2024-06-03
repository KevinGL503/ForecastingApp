""" This File contains functions used to get the current generation/load/pricing
    conditions in the ERCOT"""

import requests
import pandas as pd
import json
from datetime import datetime
import pytz

def get_curr_fuel():
    """
    This function retrieves current day fuel data for wind and solar sources,
    processes the data, and returns a resampled and interpolated DataFrame.
    :return: a DataFrame containing the current fuel mix data for wind and solar
    resampled in 15 minutes intervals
    """

    fuels = requests.get('https://www.ercot.com/api/1/services/read/dashboards/fuel-mix.json')
    cst = pytz.timezone('America/Chicago')
    data = fuels.json()['data'][datetime.strftime(datetime.now(cst), "%Y-%m-%d")]
    current = pd.DataFrame()

    for s in ['Wind', 'Solar']:
        rows = []
        for time, sources in data.items():
            for source, types in sources.items():
                if source == s:
                    this_row = {'TS': time}
                    this_row.update({'Fuel':source})
                    this_row.update(types)
                    rows.append(this_row)
        curr = pd.DataFrame(rows)

        if current.empty:
            current['TS'] = curr['TS'].copy()
        current[s] = curr['gen']

    current['TS'] = pd.to_datetime(current['TS'])
    current['TS'] = current['TS'].apply(lambda x: x - pd.DateOffset(seconds=x.second) + pd.DateOffset(minutes=1))
    current.set_index('TS', inplace=True)
    current = current.resample('15min').asfreq().interpolate(method='linear')
    current = current.bfill()
    return current

def get_curr_load():
    """
    The function `get_curr_load` retrieves and processes current day electricity
    demand data from ERCOT.
    :return: a DataFrame containing the timestamped load
    """
    load = requests.get('https://www.ercot.com/api/1/services/read/dashboards/supply-demand.json')
    data1 = load.json()['data']
    rows = []
    for patch in data1:
        this_row = {'TS':patch['timestamp']}
        this_row.update({'Load':patch['demand']})
        rows.append(this_row)

    demand = pd.DataFrame(rows)
    demand['TS'] = pd.to_datetime(demand['TS'])
    demand.set_index('TS', inplace=True)
    return demand


def get_curr_price(zone):
    """
    This function retrieves current day electricity prices data from ERCOT
    :return: a DataFrame containing the timestamped prices
    """
    prices = requests.get("https://www.ercot.com/api/1/services/read/dashboards/system-wide-prices.json")
    data2 = prices.json()['rtSppData']
    rows = []
    for patch in data2:
        this_row = {'TS':patch['timestamp']}
        this_row.update({'Price':patch[f'{zone}']})
        rows.append(this_row)

    price = pd.DataFrame(rows)
    price['TS'] = pd.to_datetime(price['TS'])
    price.set_index('TS', inplace=True)
    return price


def get_curr_cond(zone='hbBusAvg'):
    """
    This function retrieves current fuel data, load data, and price data, processes
    and calculates various features.
    :return: a DataFrame containing the columns 'Day', 'Hour', 'Price', 'Wind', 
    'Solar', 'Load', 'Prev_Load', 'Net_Load', and 'Total_Renew'.
    """

    df = get_curr_fuel()
    load = get_curr_load()
    price = get_curr_price(zone)

    df['Load'] = load['Load']
    df['Price'] = price['Price']

    df['Day'] = df.index.weekday
    df['Hour'] = df.index.hour

    df['Prev_Load'] = df['Load'].shift(1)
    df['Net_Load'] = df['Load'] - df['Wind'] - df['Solar']
    df['Total_Renew'] = df['Wind'] + df['Solar']
    df['Month'] = df.index.month
    
    return df[['Day', 'Hour', 'Price', 'Wind', 'Solar', 'Load', 'Prev_Load', 'Net_Load', 'Total_Renew', 'Month']]

