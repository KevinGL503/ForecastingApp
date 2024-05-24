from tpot import TPOTRegressor
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
import combine_data as CD
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
import pandas as pd
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
# %% Split Training data
X = data.drop(["Price"], axis=1)
y = data["Price"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
#use GradientBoost to find top 10 features and use those for TPOT
print("Running GB to find top 10 features")
gb_model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42)
gb_model.fit(X_train, y_train)
gb_pred = gb_model.predict(X_test)
mse = mean_squared_error(y_test, gb_pred)
r2 = r2_score(y_test, gb_pred)
print(f'GB Model mse: {mse}, r2: {r2}')
"""
importances = gb_model.feature_importances_
features = X.columns
feature_importance = pd.DataFrame(list(zip(features, importances)), columns=["feature", "importance"])
feature_importance = feature_importance.sort_values(by="importance", ascending=False)
top_features = feature_importance.head(10)
X_train = X_train[top_features["feature"]]
X_test = X_test[top_features["feature"]]
"""
# %% Train TPOT Model
print("Running TPOT model")
model = TPOTRegressor(generations=10, population_size=200, verbosity=4, random_state=42)
model.fit(X_train, y_train)
print(model.score(X_test, y_test))
tpot_pred = model.predict(X_test)
# Evaluate the model
mse = mean_squared_error(y_test, tpot_pred)
r2 = r2_score(y_test, tpot_pred)
print(f'TPOT Model mse: {mse}, r2: {r2}')
model.export('models/scripts/tpot_price_pipeline.py')