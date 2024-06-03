import models.scripts.combine_data as cd
import models.scripts.get_curr_cond as cc
import pandas as pd
import numpy as np

def test_get_fuel_rtm_demand_data():
    fuel, prices, demand = cd.get_fuel_rtm_demand_data()
    assert isinstance(fuel, pd.DataFrame)
    assert isinstance(prices, pd.DataFrame)
    assert isinstance(demand, pd.DataFrame)
    assert np.issubdtype(fuel.index.values[0].dtype, np.datetime64)
    assert np.issubdtype(prices.index.values[0].dtype, np.datetime64)
    assert np.issubdtype(demand.index.values[0].dtype, np.datetime64)

def test_get_curr_cond():
    df = cc.get_curr_cond()
    assert isinstance(df, pd.DataFrame)
    assert (df.columns.values.tolist() == ['Day', 'Hour', 'Price', 'Wind', 'Solar', 'Load', 'Prev_Load', 'Net_Load', 'Total_Renew'])