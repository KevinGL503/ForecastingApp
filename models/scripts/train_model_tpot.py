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

#%% Train TPOTRegressor Model
from tpot import TPOTRegressor
tpot_model = TPOTRegressor(generations=5,population_size=20,verbosity=2,random_state=42)
tpot_model.fit(X_train,y_train)

#evaluate model
y_pred = tpot_model.predict(X_test)
mse = mean_squared_error(y_test,y_pred)
print(f"MSE of TPOT Regressor model {mse}")
# %% Save the trained models
with open('./models/models_tpot.pkl', 'wb') as models:
    pickle.dump(tpot_model, models)

# %%
