#%%
import pandas as pd
import pytest
import autokeras as ak
from datetime import datetime
import combine_data as CD
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
import pickle
##This upto split data function is all data preprocessing needed to train the models
def get_data(months, price_point, fuels):
    fuel, prices, demand = CD.get_fuel_rtm_demand_data(months, price_point, fuels)
    return fuel, prices, demand

def combine_and_prep_data(fuel, prices, demand, start_date, end_date):
    data = CD.combined_data(fuel, prices, demand, start_date, end_date)
    data = CD.prep_data(data)
    return data

def visualize_data(data):
    px.line(data.groupby(['Day','Hour'])['Total_Renew'].mean().reset_index(),x='Hour', \
            y='Total_Renew',color='Day', title="Avg Hourly Solar Gen By Day")
    px.line(data.groupby(['Day', 'Hour'])['Price'].mean().reset_index(), x='Hour',
            y='Price', color='Day', title='Avg Hourly Price By Day')
    px.line(data.groupby(['Hour', 'Day'])['Load'].mean().reset_index(), x='Hour',
            y='Load', color='Day', title='Avg Hourly Load By Day')
# %% Split Training data function
def split_data(data):
    X = data.drop(["Price"], axis=1)
    y = data["Price"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test

#train autokeras model
def train_autokeras_model(X_train, y_train):
    auto_model = ak.StructuredDataRegressor(max_trials=10)
    auto_model.fit(X_train, y_train)
    return auto_model

#generalized evaluation function for models
def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    return mse, r2
@pytest.fixture
def sample_data():
    # Generate sample data
    fuel = pd.DataFrame({
        'Date': pd.date_range(start='2023-01-01', end='2023-12-31', freq='H'),
        'Wind': [0.5] * 8760,
        'Solar': [0.3] * 8760
    })
    prices = pd.DataFrame({
        'Date': pd.date_range(start='2023-01-01', end='2023-12-31', freq='H'),
        'HB_BUSAVG': [50.0] * 8760
    })
    demand = pd.DataFrame({
        'Date': pd.date_range(start='2023-01-01', end='2023-12-31', freq='H'),
        'Load': [100.0] * 8760
    })
    start_date = datetime.strptime('05/01/2023', '%m/%d/%Y')
    end_date = datetime.strptime('08/01/2023', '%m/%d/%Y')
    data = combine_and_prep_data(fuel, prices, demand, start_date, end_date)
    return data

def test_autokeras_model(sample_data):
    X_train, X_test, y_train, y_test = split_data(sample_data)
    model = train_autokeras_model(X_train, y_train)
    mse, r2 = evaluate_model(model, X_test, y_test)
    assert isinstance(mse, float)
    assert isinstance(r2, float)
    assert mse >= 0
    assert r2 >= -1 and r2 <= 1
# %% Main function, runs data preprocessing, model training, and model evaluation
def main():
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug']
    price_point = ['HB_BUSAVG']
    fuels = ['Wind', 'Solar']
    fuel, prices, demand = get_data(months, price_point, fuels)
    
    start_date = datetime.strptime('05/01/2023', '%m/%d/%Y')
    end_date = datetime.strptime('08/01/2023', '%m/%d/%Y')
    data = combine_and_prep_data(fuel, prices, demand, start_date, end_date)
    
    visualize_data(data)
    
    X_train, X_test, y_train, y_test = split_data(data)

    auto_model = train_autokeras_model(X_train, y_train)
    mse, r2 = evaluate_model(auto_model, 'Auto Keras', X_test, y_test)
    print(f'Auto Keras: MSE={mse}, R2={r2}')
    
    with open('./models/models.pkl', 'wb') as models:
        pickle.dump(auto_model, models)
if __name__ == '__main__':
    main()