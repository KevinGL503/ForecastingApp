from sklearn.neural_network import MLPRegressor
from datetime import datetime
from sklearn.model_selection import train_test_split
import plotly.express as px
import scripts.combine_data as CD
from sklearn.metrics import mean_squared_error, r2_score
import pickle
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
#use NN Regression model to predict the target value
def train_model(X_train, y_train):
    nn_model = MLPRegressor(hidden_layer_sizes=(100, 100), max_iter=1000, random_state=42)
    nn_model.fit(X_train, y_train)
    return nn_model
#evaluate the model
def evaluate_model(nn_model, X_test, y_test):
    y_pred = nn_model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    return mse, r2
#save the model
def save_model(nn_model, filepath):
    with open(filepath, 'wb') as models:
        pickle.dump(nn_model, models)
# Create the neural network regression model
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
    
    nn = train_model(X_train, y_train)
    
    mse, r2 = evaluate_model(nn, X_test, y_test)
    print(f"MSE of TPOT Regressor model: {mse}")
    print(f"R2 Score: {r2}")
    
    save_model(nn, './models/models_nn.pkl')

if __name__ == "__main__":
    main()