"""This File contains the functions to collect historical data from ERCOT for 
    training the models"""

import requests
import zipfile
import io
import pandas as pd
import os

def fix_rtm_prices(df1):

    df = df1.copy()
    df['Hour'] = df.apply(lambda x: x['Delivery Hour']-1, axis=1)
    df['Minute']= df.apply(lambda x: 0 if x['Delivery Interval'] == 4 else \
                           (x['Delivery Interval'] * 15), axis=1)
    df.loc[df['Minute'] == 0, ['Hour']] += 1
    df['Delivery Date'] = pd.to_datetime(df['Delivery Date'])

    df['TS'] = df.apply(lambda x: x['Delivery Date'] + \
                pd.DateOffset(hours=x['Hour'], minutes=x['Minute']), axis=1)
    df['Day']= df.apply(lambda x: x['TS'].weekday(), axis=1)
    df.drop(columns=['Repeated Hour Flag', 'Delivery Hour', 'Delivery Date'],\
             inplace=True)
    df.reset_index(inplace=True)

    df['Hour'] = df.apply(lambda x: int(x['TS'].hour), axis=1)

    return df[['TS', 'Day', 'Hour', 'Settlement Point Name', \
               'Settlement Point Price', 'Settlement Point Type']]


def get_rtm_yearly(url, year):
    #https://www.ercot.com/misdownload/servlets/mirDownload?doclookupId=969805139
    r = requests.get(url)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    unzipped = z.read(z.infolist()[0]) 
    excel_file = io.BytesIO(unzipped)
    df1 = pd.read_excel(excel_file, sheet_name=None)


    for m in df1.keys():
        print(f'exec {m}')
        df = df1[m].copy()
        df_all = fix_rtm_prices(df)
        try:
            df_all.to_csv(f'./data/{year}/RTM/{m}Rtm.csv', index=False)
        except:
            if not os.path.exists(f'./data/{year}/RTM/'):
                os.makedirs(f'./data/{year}/RTM/')
            df_all.to_csv(f'./data/{year}/RTM/{m}Rtm.csv', index=False)
        print(f'Saved {m}_rmt.csv')


def get_load(url):
    r = requests.get(url)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    unzipped = z.read(z.infolist()[0]) 
    excel_file = io.BytesIO(unzipped)
    dfs = pd.read_excel(excel_file, sheet_name=None)

    df = dfs['Sheet1'].copy()
    df.rename(columns={'Hour Ending': 'TS'}, inplace=True)
    df['Hour'] = df['TS'].apply(lambda x: int(x[-5:-3])-1)
    df['TS'] = df.apply(lambda x: pd.to_datetime(x['TS'][0:-5]) + \
                        pd.DateOffset(hours=x['Hour']), axis=1)
    df['Day'] = df['TS'].apply(lambda x: x.weekday())

    return df[['TS', 'Day', 'Hour', 'ERCOT', 'COAST', 'EAST', 'FWEST', 'NORTH',\
                'NCENT', 'SOUTH', 'SCENT', 'WEST']]


def get_monthly_load(url, year):
    df = get_load(url)

    months = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', \
                  7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}
        
    for n,m in months.items():
        month_df = df.apply(lambda x: \
                                x['TS'].month == n, axis=1)
        df_m = df[month_df].copy()

        try:
            df_m.to_csv(f'./data/{year}/Demand/{m}Demand.csv', index=False)
        except:
            if not os.path.exists(f'./data/{year}/Demand/'):
                os.makedirs(f'./data/{year}/Demand/')
            df_m.to_csv(f'./data/{year}/Demand/{m}Demand.csv', index=False)
        print(f'Saved demand{m}.csv')


def get_files_list(url):
    r = requests.get(url)
    extracted_data = [
        {
            "DocID": doc["Document"]["DocID"],
            "ReportName": doc["Document"]["ReportName"],
            "FriendlyName":doc["Document"]["FriendlyName"]
        }
        for doc in r.json()["ListDocsByRptTypeRes"]["DocumentList"]
    ]

    df_urls = pd.DataFrame(extracted_data)
    df_urls['DocUrl'] = df_urls.apply(lambda row: \
        'https://www.ercot.com/misdownload/servlets/mirDownload?doclookupId=' + \
            str(row['DocID']), axis=1)
    
    return df_urls


def get_solar_wind_data(year):
    url = 'https://www.ercot.com/misapp/servlets/IceDocListJsonWS' +\
                     '?reportTypeId=13424&_=1712261041562'
    
    df_urls = get_files_list(url)
    this_file = df_urls['FriendlyName'].apply(lambda x: str(year) in x)
    year_file = requests.get(df_urls[this_file]['DocUrl'].values[0])

    dfs = pd.read_excel(io.BytesIO(year_file.content), sheet_name=None)
    fuel_name = {'Wind': 'WIND', 'Solar': 'PVGR'}
    for fuel in ['Wind','Solar']:
        df_wind = dfs[f'{fuel} Data'].copy()
        df_wind['Time (Hour-Ending)'] = pd.to_datetime(\
            df_wind['Time (Hour-Ending)']) - pd.DateOffset(hours=1)

        months = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', \
                  7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}
        
        for n,m in months.items():
            month_df = df_wind.apply(lambda x: \
                                    x['Time (Hour-Ending)'].month == n, axis=1)
            df = df_wind[month_df].copy()
            df.rename(columns={'Time (Hour-Ending)':'TS', \
                        f'ERCOT.{fuel_name[fuel]}.GEN':f'{fuel}'}, inplace=True)
            df['Day'] = df['TS'].apply(lambda x: x.weekday())
            df['Hour'] = df['TS'].apply(lambda x: x.hour)
            df = df[['TS', 'Day', 'Hour', 'ERCOT.LOAD', f'{fuel}']]

            try:
                df.to_csv(f'./data/{year}/Fuel/{m}{fuel}.csv', index=False)
            except: 
                if not os.path.exists(f'./data/{year}/Fuel/'):
                    os.makedirs(f'./data/{year}/Fuel/')
                df.to_csv(f'./data/{year}/Fuel/{m}{fuel}.csv', index=False)
            print(f'Saved: {m}{fuel}.csv')


if __name__ == "__main__":
    get_rtm_yearly('https://www.ercot.com/misdownload/servlets/mirDownload?doclookupId=969805139', 2023)
    get_solar_wind_data(2023)
    get_monthly_load('https://www.ercot.com/files/docs/2023/02/09/Native_Load_2023.zip', 2023)

