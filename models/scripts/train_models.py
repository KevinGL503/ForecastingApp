"""This File uses Linear Regression, Decision Tree Regression, Random Forest Regression, and Gradient Boosting Regression to predict energy prices"""
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
from sklearn.model_selection import GridSearchCV
def get_data(months, price_point, fuels):
    """This function gets the data needed for training the model
    :param months: The months to get data for
    :param price_point: The price point to get data for
    :param fuels: The fuels to get data for
    :return: fuel, prices, demand"""
    fuel, prices, demand = CD.get_fuel_rtm_demand_data(months, price_point, fuels)
    return fuel, prices, demand

def combine_and_prep_data(fuel, prices, demand, start_date, end_date):
    """This function combines and prepares the data for training the model
    :param fuel: The fuel data
    :param prices: The price data
    :param demand: The demand data
    :param start_date: The start date for the data
    :param end_date: The end date for the data
    :return: data"""

    data = CD.combined_data(fuel, prices, demand, start_date, end_date)
    data = CD.prep_data(data)
    return data

def visualize_data(data):
    """This function visualizes the data
    :param data: The data to visualize"""
    
    px.line(data.groupby(['Day','Hour'])['Total_Renew'].mean().reset_index(),x='Hour', \
            y='Total_Renew',color='Day', title="Avg Hourly Solar Gen By Day")
    px.line(data.groupby(['Day', 'Hour'])['Price'].mean().reset_index(), x='Hour',
            y='Price', color='Day', title='Avg Hourly Price By Day')
    px.line(data.groupby(['Hour', 'Day'])['Load'].mean().reset_index(), x='Hour',
            y='Load', color='Day', title='Avg Hourly Load By Day')
def split_data(data):
    """This function splits the data into training and testing sets
    :param data: The data to split
    :return: X_train, X_test, y_train, y_test"""

    X = data.drop(["Price"], axis=1)
    y = data["Price"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test

def train_linear_model(X_train, y_train):
    """This function trains a linear regression model
    :param X_train: The training data
    :param y_train: The training labels
    :return: linear_model"""

    linear_model = LinearRegression()
    linear_model.fit(X_train, y_train)
    return linear_model

def train_tree_model(X_train, y_train):
    """This function trains a decision tree regression model
    :param X_train: The training data
    :param y_train: The training labels
    :return: tree"""

    tree = DecisionTreeRegressor(max_depth=10)
    tree.fit(X_train, y_train)
    return tree

def train_forest_model(X_train, y_train):
    """This function trains a random forest regression model
    :param X_train: The training data
    :param y_train: The training labels
    :return: forest"""

    forest = RandomForestRegressor(n_estimators=100, max_depth=5, random_state=42)
    forest.fit(X_train, y_train)
    return forest

def train_gb_model(X_train, y_train):
    """This function trains a gradient boosting regression model
    :param X_train: The training data
    :param y_train: The training labels
    :return: gb_model"""

    gb_model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42)
    gb_model.fit(X_train, y_train)
    return gb_model
def improve_model(X_train, y_train, model):
    """This function improves the model by tuning hyperparameters
    :param X_train: The training data
    :param y_train: The training labels
    :param model: The model to improve
    :return: model"""
    model = model
    param_grid = {
        'n_estimators': [50, 100, 200],
        'max_depth': [None, 10, 20, 30],
        'min_samples_split': [2, 5, 10]
    }
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=3, scoring='neg_mean_squared_error')
    grid_search.fit(X_train, y_train)
    return grid_search.best_estimator_

def evaluate_model(model, X_test, y_test):
    """This function evaluates the model using the test data
    :param model: The model to evaluate
    :param X_test: The test data
    :param y_test: The test labels
    :return: mse, r2"""

    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    return mse, r2

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
    
    print('Training models')
    linear_model = train_linear_model(X_train, y_train, 'Linear')
    tree = train_tree_model(X_train, y_train, 'Tree')
    forest = train_forest_model(X_train, y_train, 'Forest')
    gb_model = train_gb_model(X_train, y_train, 'Gradient Boosting')
    
    #imrpove models
    print('Improving models')
    forest = improve_model(X_train, y_train, forest)
    gb_model = improve_model(X_train, y_train, gb_model)
    linear_model = improve_model(X_train, y_train, linear_model)
    tree = improve_model(X_train, y_train, tree)

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
if __name__ == '__main__':
    main()