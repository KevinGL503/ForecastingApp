import pytest
import pandas as pd
from datetime import datetime
import train_models as TM
def get_some_data():
    # Assuming you have some way to get these dataframes
    fuel, prices, demand = TM.get_data()
    start_date = datetime.strptime('05/01/2023', '%m/%d/%Y')
    end_date = datetime.strptime('08/01/2023', '%m/%d/%Y')
    data = TM.combine_and_prep_data(fuel, prices, demand, start_date, end_date)
    return data
def get_some_data_and_model():
    # Assuming you have some way to get these dataframes and a model
    data = get_some_data()
    X_train, X_test, y_train, y_test = TM.split_data(data)
    model = TM.train_linear_model(X_train, y_train, 'Linear')
    return X_test, y_test, model
def test_get_data():
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug']
    price_point = ['HB_BUSAVG']
    fuels = ['Wind', 'Solar']
    fuel, prices, demand = TM.get_data(months, price_point, fuels)
    assert isinstance(fuel, pd.DataFrame)
    assert isinstance(prices, pd.DataFrame)
    assert isinstance(demand, pd.DataFrame)

def test_combine_and_prep_data():
    # Assuming you have some way to get these dataframes
    fuel, prices, demand = get_some_data()
    start_date = datetime.strptime('05/01/2023', '%m/%d/%Y')
    end_date = datetime.strptime('08/01/2023', '%m/%d/%Y')
    data = TM.combine_and_prep_data(fuel, prices, demand, start_date, end_date)
    assert isinstance(data, pd.DataFrame)

def test_split_data():
    # Assuming you have some way to get this dataframe
    data = get_some_data()
    X_train, X_test, y_train, y_test = TM.split_data(data)
    assert isinstance(X_train, pd.DataFrame)
    assert isinstance(X_test, pd.DataFrame)
    assert isinstance(y_train, pd.Series)
    assert isinstance(y_test, pd.Series)

def test_train_linear_model():
    # Assuming you have some way to get these dataframes
    X_train, y_train = get_some_data()
    model = TM.train_linear_model(X_train, y_train, 'Linear')
    assert model is not None

def test_train_tree_model():
    # Assuming you have some way to get these dataframes
    X_train, y_train = get_some_data()
    model = TM.train_tree_model(X_train, y_train, 'Tree')
    assert model is not None

def test_train_forest_model():
    # Assuming you have some way to get these dataframes
    X_train, y_train = get_some_data()
    model = TM.train_forest_model(X_train, y_train, 'Forest')
    assert model is not None

def test_train_gb_model():
    # Assuming you have some way to get these dataframes
    X_train, y_train = get_some_data()
    model = TM.train_gb_model(X_train, y_train, 'Gradient Boosting')
    assert model is not None

def test_evaluate_model():
    # Assuming you have some way to get these dataframes and a model
    X_test, y_test, model = get_some_data_and_model()
    mse, r2 = TM.evaluate_model(model, 'Model', X_test, y_test)
    assert isinstance(mse, float)
    assert isinstance(r2, float)