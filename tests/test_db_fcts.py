import api.updater.day_conds as dc 
import pandas as pd
import numpy as np
from datetime import datetime

def test_get_today_predicted_fuel():
    df = dc.get_today_predicted_fuel()
    assert isinstance(df, pd.DataFrame)
    assert df.columns.values.tolist() == ['TS', 'Wind', 'Solar']
    assert pd.to_datetime(df['TS'].values[0]).day == datetime.now().day
    assert pd.to_datetime(df['TS'].values[0]).month == datetime.now().month

def test_get_today_predicted_load():
    df = dc.get_today_predicted_load()
    assert isinstance(df, pd.DataFrame)
    assert df.columns.values.tolist() == ['TS', 'Load']
    assert pd.to_datetime(df['TS'].values[0]).day == datetime.now().day
    assert pd.to_datetime(df['TS'].values[0]).month == datetime.now().month

def test_get_today_cond():
    df = dc.get_today_cond()
    assert df.isna().sum().sum() == 0
    assert np.issubdtype(df.index.values[0].dtype, np.datetime64)
    assert df.columns.values.tolist() == ['Day', 'Hour', 'Wind', 'Solar', \
                    'Load', 'Prev_Load', 'Net_Load', 'Total_Renew', 'Month']