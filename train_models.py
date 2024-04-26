#%%
import pandas as pd
from datetime import datetime
import scripts.combine_data as CD
#%% Get fuel, prices, and demand data
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
price_point = ['HB_BUSAVG']
fuels = ['Wind', 'Solar']
fuel, prices, demand = CD.get_fuel_rtm_demand_data(months, price_point, fuels)

# %% Combine data into a merged df given a date range
start_date = datetime.strptime('02/01/2023', '%m/%d/%Y')
end_date = datetime.strptime('06/01/2023', '%m/%d/%Y')
data = CD.combined_data(fuel, prices, demand, start_date, end_date)

# %% Feature engineering and outlier analysis 
data['Prev_Load'] = data['Load'].shift(1)
data['Net_Load'] = data['Load'] - data['Wind'] - data['Solar']
data.dropna(inplace=True)

std = data['Price'].std()
mean = data['Price'].mean()
median = data['Price'].median()
ub = mean + (3*std)
lb = mean - (3*std)
data['Price'] = data['Price'].apply(lambda x: median if x < lb or x > ub else x)

# %%
