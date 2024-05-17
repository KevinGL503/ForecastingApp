import pytest
from datetime import datetime
from train_model_tpot import get_data, combine_data, split_data, train_model, evaluate_model, save_model
import combine_data as CD
import os

@pytest.fixture
def sample_data():
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug']
    price_point = ['HB_BUSAVG']
    fuels = ['Wind', 'Solar']
    fuel, prices, demand = get_data(months, price_point, fuels)
    start_date = datetime.strptime('05/01/2023', '%m/%d/%Y')
    end_date = datetime.strptime('08/01/2023', '%m/%d/%Y')
    data = combine_data(fuel, prices, demand, start_date, end_date)
    return data

def test_get_data():
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug']
    price_point = ['HB_BUSAVG']
    fuels = ['Wind', 'Solar']
    fuel, prices, demand = get_data(months, price_point, fuels)
    assert not fuel.empty
    assert not prices.empty
    assert not demand.empty

def test_combine_data(sample_data):
    assert not sample_data.empty

def test_split_data(sample_data):
    X_train, X_test, y_train, y_test = split_data(sample_data)
    assert len(X_train) > 0
    assert len(X_test) > 0
    assert len(y_train) > 0
    assert len(y_test) > 0

def test_train_model(sample_data):
    X_train, X_test, y_train, y_test = split_data(sample_data)
    model = train_model(X_train, y_train)
    assert model is not None

def test_evaluate_model(sample_data):
    X_train, X_test, y_train, y_test = split_data(sample_data)
    model = train_model(X_train, y_train)
    mse, r2 = evaluate_model(model, X_test, y_test)
    assert mse >= 0
    assert r2 <= 1

def test_save_model(sample_data):
    X_train, X_test, y_train, y_test = split_data(sample_data)
    model = train_model(X_train, y_train)
    filepath = './models/models_tpot_test.pkl'
    save_model(model, filepath)
    assert os.path.exists(filepath)
    os.remove(filepath)
