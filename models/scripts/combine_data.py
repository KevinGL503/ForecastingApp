""" This file contains the functions used to read and combine data for model 
	training purposes and other"""

import pandas as pd

def get_fuel_rtm_demand_data(month=['Jan'], rtm_point=['HB_BUSAVG'], fuels=['Wind', 'Solar']):
	"""
    The function `get_fuel_rtm_demand_data` reads RTM, fuel (Solar and Wind), and
    demand data for specified months and RTM points, and returns combined dataframes
    for each type of data.

    :param month: months for which to read the data as list of strings
    :param rtm_point: settlement points for which to read the rtm prices, as a 
	list of strings. Set to 'HB_BUSAVG' by default
    :param fuels: Fuels for which to read the data as a list of strings
    :return: The function `get_fuel_rtm_demand_data` is returning three DataFrames:
    `combined_fuel`, `combined_rtm`, and `combined_demand`
    """
	combined_rtm = pd.DataFrame()
	combined_fuel = pd.DataFrame()
	combined_demand = pd.DataFrame()

	for m in month:
		#Get rtm data
		rtm_data = pd.read_csv(f'./data/2023/RTM/{m}Rtm.csv', parse_dates=['TS'])
		for zone in rtm_point:
			hb_data = rtm_data.loc[rtm_data['Settlement Point Name'] == zone].copy()
			hb_data.rename(columns={'Settlement Point Price':'Price'}, inplace=True)
			hb_data.set_index(["TS"], inplace=True)
			combined_rtm = pd.concat([combined_rtm, hb_data])

		# Get Solar and Wind Data
		solar_df = pd.read_csv(f'./data/2023/Fuel/{m}Solar.csv', parse_dates=['TS'])
		solar_df.set_index(['TS'], inplace=True)
		df_fuel = pd.read_csv(f'./data/2023/Fuel/{m}Wind.csv', parse_dates=['TS'])
		df_fuel.set_index(['TS'], inplace=True)
		df_fuel['Solar'] = solar_df['Solar']
		combined_fuel = pd.concat([combined_fuel, df_fuel])

		#Get demand data
		demand = pd.read_csv(f'./data/2023/Demand/{m}Demand.csv', parse_dates=['TS'])
		demand.set_index('TS', inplace=True)
		combined_demand = pd.concat([combined_demand, demand])

	return combined_fuel, combined_rtm, combined_demand

def combined_data(fuel, rtm, demand, s_d, e_d):
	"""
	The function `combined_data` combines data from different sources (RTM prices
	,fuel, demand) based on a specified time range into a single df.
	
	:param fuel: The fuel dataframe
	:param rtm: the rtm price dataframe
	:param demand: the demand dataframe
	:param s_d: start date and time for the data you want to extract from
	the datasets
	:param e_d: end date and time for the data you want to extract from
	the datasets
	:return: The function `combined_data` returns a combined DataFrame containing
	data from the `rtm`, `fuel`, and `demand` DataFrames for the specified time
	period between `s_d` and `e_d`. The combined DataFrame includes columns for
	'Day', 'Hour', 'Price', 'Wind', 'Solar', and 'Load' having timestamps in
	15 mins intervals as index.
	"""
	df = rtm[(rtm.index >= s_d) & (rtm.index < e_d)][['Day', 'Hour', 'Price', 'Settlement Point Name']].copy()
	combined_df = df.copy()

	df = fuel.resample('15min').asfreq().interpolate(method='linear')
	combined_df[['Wind', 'Solar']] = df[(df.index >= s_d) & (df.index < e_d)][['Wind', 'Solar']]

	df = demand.resample('15min').asfreq().interpolate(method='linear')
	combined_df['Load'] = df[(df.index >= s_d) & (df.index < e_d)]['ERCOT']

	return combined_df

def prep_data(data):
	"""
	The function `prep_data` performs feature engineering, outlier analysis, and
	data preprocessing on the data.
	
	:param data: df containing the combined data 
	:return: The function `prep_data` is returning the modified data after
	performing feature engineering, outlier analysis, and data preprocessing steps.
	"""
	# Feature engineering and outlier analysis 
	data['Prev_Load'] = data['Load'].shift(1)
	data['Net_Load'] = data['Load'] - data['Wind'] - data['Solar']
	data['Total_Renew'] = data['Solar'] + data['Wind']
	data['Month'] = data.index.month
	data.dropna(inplace=True)

	std = data['Price'].std()
	mean = data['Price'].mean()
	median = data['Price'].median()
	ub = mean + (3*std)
	lb = mean - (3*std)
	data['Price'] = data['Price'].apply(lambda x: median if x < lb or x > ub else x)

	return data