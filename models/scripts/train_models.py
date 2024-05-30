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
#%% Get fuel, prices, and demand data
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug']
price_point = ['HB_BUSAVG', 'HB_SOUTH', 'HB_WEST', 'HB_NORTH', 'HB_HOUSTON']
fuels = ['Wind', 'Solar']
start_date = datetime.strptime('05/01/2023', '%m/%d/%Y')
end_date = datetime.strptime('08/01/2023', '%m/%d/%Y')
fuel, prices, demand = CD.get_fuel_rtm_demand_data(months, price_point, fuels)
data = CD.combined_data(fuel, prices, demand, start_date, end_date)
# %%
data1 = CD.prep_data(data)
for point in price_point:
    data = data1[data1['Settlement Point Name'] == point].copy()
    X = data.drop(["Price", "Settlement Point Name"], axis=1)
    y = data["Price"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


    linear_model = LinearRegression()
    linear_model.fit(X_train,y_train)
    y_pred = linear_model.predict(X_test)


    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f'Linear mse: {mse}, r2: {r2}')

    tree = DecisionTreeRegressor(max_depth=10)
    tree.fit(X_train, y_train)
    # Predictions
    tree_pred = tree.predict(X_test)

    # Evaluate the model
    mse = mean_squared_error(y_test, tree_pred)
    r2 = r2_score(y_test, tree_pred)
    print(f'Decision tree mse: {mse}, r2: {r2}')

    forest = RandomForestRegressor(n_estimators=100, max_depth=5, random_state=42)
    forest.fit(X_train, y_train)
    forest_pred = forest.predict(X_test)

    # Evaluate the model
    mse = mean_squared_error(y_test, forest_pred)
    r2 = r2_score(y_test, forest_pred)
    print(f'Forest mse: {mse}, r2: {r2}')

    gb_model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42)
    gb_model.fit(X_train, y_train)
    gb_pred = gb_model.predict(X_test)

    mse = mean_squared_error(y_test, forest_pred)
    r2 = r2_score(y_test, forest_pred)
    print(f'Gradient Boosting mse: {mse}, r2: {r2}')

    with open(f'./models/{point}_models.pkl', 'wb') as models:
        pickle.dump(linear_model, models)
        pickle.dump(tree, models)
        pickle.dump(forest, models)
        pickle.dump(gb_model, models)