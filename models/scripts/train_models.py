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
price_point = ['HB_BUSAVG']
fuels = ['Wind', 'Solar']
fuel, prices, demand = CD.get_fuel_rtm_demand_data(months, price_point, fuels)

# %% Combine data into a merged df given a date range
start_date = datetime.strptime('05/01/2023', '%m/%d/%Y')
end_date = datetime.strptime('08/01/2023', '%m/%d/%Y')
data = CD.combined_data(fuel, prices, demand, start_date, end_date)
data = CD.prep_data(data)
# %% Some data visualization 
px.line(data.groupby(['Day','Hour'])['Total_Renew'].mean().reset_index(),x='Hour', \
        y='Total_Renew',color='Day', title="Avg Hourly Solar Gen By Day")
px.line(data.groupby(['Day', 'Hour'])['Price'].mean().reset_index(), x='Hour',
        y='Price', color='Day', title='Avg Hourly Price By Day')
px.line(data.groupby(['Hour', 'Day'])['Load'].mean().reset_index(), x='Hour',
        y='Load', color='Day', title='Avg Hourly Load By Day')
# %% Split Training data
X = data.drop(["Price"], axis=1)
y = data["Price"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#%% Train a Linear regression model
linear_model = LinearRegression()
linear_model.fit(X_train,y_train)
y_pred = linear_model.predict(X_test)

# %% Check Linear model accuracy 
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f'Linear mse: {mse}, r2: {r2}')
#%% Train Decision Tree Regression
tree = DecisionTreeRegressor(max_depth=10)
tree.fit(X_train, y_train)
# Predictions
tree_pred = tree.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, tree_pred)
r2 = r2_score(y_test, tree_pred)
print(f'Decision tree mse: {mse}, r2: {r2}')
# %% Train random forest regression
forest = RandomForestRegressor(n_estimators=100, max_depth=5, random_state=42)
forest.fit(X_train, y_train)
forest_pred = forest.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, forest_pred)
r2 = r2_score(y_test, forest_pred)
print(f'Forest mse: {mse}, r2: {r2}')
# %% Gradient boosting regreesion model
gb_model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42)
gb_model.fit(X_train, y_train)
gb_pred = gb_model.predict(X_test)

mse = mean_squared_error(y_test, forest_pred)
r2 = r2_score(y_test, forest_pred)
print(f'Gradient Boosting mse: {mse}, r2: {r2}')
# %% Save the trained models
with open('./models/models.pkl', 'wb') as models:
    pickle.dump(linear_model, models)
    pickle.dump(tree, models)
    pickle.dump(forest, models)
    pickle.dump(gb_model, models)

# %%