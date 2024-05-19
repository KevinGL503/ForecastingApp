import pandas as pd
from datetime import datetime
import combine_data as CD
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import pickle
from tpot import TPOTRegressor
import pytest
import pandas as pd
from datetime import datetime
import combine_data as CD
from tpot import TPOTRegressor

def get_data(months, price_point, fuels):
    fuel, prices, demand = CD.get_fuel_rtm_demand_data(months, price_point, fuels)
    return fuel, prices, demand

def combine_data(fuel, prices, demand, start_date, end_date):
    data = CD.combined_data(fuel, prices, demand, start_date, end_date)
    data = CD.prep_data(data)
    return data

def visualize_data(data):
    px.line(data.groupby(['Day', 'Hour'])['Total_Renew'].mean().reset_index(), x='Hour', 
            y='Total_Renew', color='Day', title="Avg Hourly Solar Gen By Day")
    px.line(data.groupby(['Day', 'Hour'])['Price'].mean().reset_index(), x='Hour', 
            y='Price', color='Day', title='Avg Hourly Price By Day')
    px.line(data.groupby(['Hour', 'Day'])['Load'].mean().reset_index(), x='Hour', 
            y='Load', color='Day', title='Avg Hourly Load By Day')

def split_data(data):
    X = data.drop(["Price"], axis=1)
    y = data["Price"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test

def train_model(X_train, y_train):
    tpot_model = TPOTRegressor(generations=10,    # Increase the number of generations
                               population_size=100,    # Increase the population size
                               verbosity=3, 
                               random_state=42, 
                               scoring='neg_mean_squared_error',    # Use negative mean squared error for scoring
                               cv=10,    # Increase the number of cross-validation folds
                               n_jobs=-1)    # Use all available cores
    tpot_model.fit(X_train, y_train)
    return tpot_model

def evaluate_model(tpot_model, X_test, y_test):
    y_pred = tpot_model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    return mse, r2
def save_model(tpot_model, filepath):
    with open(filepath, 'wb') as models:
        pickle.dump(tpot_model, models)
@pytest.fixture
def sample_data():
    # Generate sample data in the same format as data/2023 csv files
    # Replace this with your own code to generate the sample data
    data = pd.DataFrame({
        'Date': ['2023-01-01', '2023-01-02', '2023-01-03'],
        'Hour': [1, 2, 3],
        'Total_Renew': [100, 200, 300],
        'Price': [10, 20, 30],
        'Load': [1000, 2000, 3000]
    })
    return data

def test_functions(sample_data):
    data = sample_data
    
    X_train, X_test, y_train, y_test = split_data(data)
    
    tpot_model = train_model(X_train, y_train)
    
    mse, r2 = evaluate_model(tpot_model, X_test, y_test)
    assert isinstance(mse, float)
    assert isinstance(r2, float)
    
    save_model(tpot_model, './models/models_tpot.pkl')
    tpot_model.export('./models/models_tpot.py')
def main():
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug']
    price_point = ['HB_BUSAVG']
    fuels = ['Wind', 'Solar']
    fuel, prices, demand = get_data(months, price_point, fuels)
    
    start_date = datetime.strptime('05/01/2023', '%m/%d/%Y')
    end_date = datetime.strptime('08/01/2023', '%m/%d/%Y')
    data = combine_data(fuel, prices, demand, start_date, end_date)
    
    visualize_data(data)
    
    X_train, X_test, y_train, y_test = split_data(data)
    
    tpot_model = train_model(X_train, y_train)
    
    mse, r2 = evaluate_model(tpot_model, X_test, y_test)
    print(f"MSE of TPOT Regressor model: {mse}")
    print(f"R2 Score: {r2}")
    
    save_model(tpot_model, './models/models_tpot.pkl')
    tpot_model.export('./models/models_tpot.py')

if __name__ == "__main__":
    main()
