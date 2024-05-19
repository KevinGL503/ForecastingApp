#%%
import pandas as pd
from datetime import datetime
import combine_data as CD
import plotly.express as px
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor 
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
import pickle
##This upto split data function is all data preprocessing needed to train the models, TODO: implement this into separate functions

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

#%% Train a Linear regression model function
def train_linear_model(X_train, y_train, name):
    linear_model = LinearRegression()
    linear_model.fit(X_train, y_train)
    return linear_model

#%% Train Decision Tree Regression function
def train_tree_model(X_train, y_train, name):
    tree = DecisionTreeRegressor(max_depth=10)
    tree.fit(X_train, y_train)
    return tree

# %% Train random forest regression function
def train_forest_model(X_train, y_train, name):
    forest = RandomForestRegressor(n_estimators=100, max_depth=5, random_state=42)
    forest.fit(X_train, y_train)
    return forest

# %% Gradient boosting regreesion model function
def train_gb_model(X_train, y_train, name):
    gb_model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42)
    gb_model.fit(X_train, y_train)
    return gb_model

#generalized evaluation function for models
def evaluate_model(model, name, X_test, y_test):
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    return mse, r2

# %%
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
    #do multithreading here
    
    linear_model = train_linear_model(X_train, y_train, 'Linear')
    tree = train_tree_model(X_train, y_train, 'Tree')
    forest = train_forest_model(X_train, y_train, 'Forest')
    gb_model = train_gb_model(X_train, y_train, 'Gradient Boosting')
    
    mse, r2 = evaluate_model(linear_model, 'Linear', X_test, y_test)
    print(f'Linear Model: MSE={mse}, R2={r2}')
    
    mse, r2 = evaluate_model(tree, 'Tree', X_test, y_test)
    print(f'Tree Model: MSE={mse}, R2={r2}')
    
    mse, r2 = evaluate_model(forest, 'Forest', X_test, y_test)
    print(f'Forest Model: MSE={mse}, R2={r2}')
    
    mse, r2 = evaluate_model(gb_model, 'Gradient Boosting', X_test, y_test)
    print(f'Gradient Boosting Model: MSE={mse}, R2={r2}')
    
    with open('./models/models.pkl', 'wb') as models:
        pickle.dump(linear_model, models)
        pickle.dump(tree, models)
        pickle.dump(forest, models)
        pickle.dump(gb_model, models)