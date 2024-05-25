"""This file uses the TPOT library to train a model to predict energy prices"""

from tpot import TPOTRegressor
from sklearn.metrics import mean_squared_error, r2_score
import combine_data as CD
from datetime import datetime
from sklearn.model_selection import train_test_split
import pandas as pd
import pickle
import numpy as np
import matplotlib.pyplot as plt
def get_data():
    """This function gets the data needed for training the model"""

    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug']
    price_point = ['HB_BUSAVG']
    fuels = ['Wind', 'Solar']
    fuel, prices, demand = CD.get_fuel_rtm_demand_data(months, price_point, fuels)

    start_date = datetime.strptime('05/01/2023', '%m/%d/%Y')
    end_date = datetime.strptime('08/01/2023', '%m/%d/%Y')
    data = CD.combined_data(fuel, prices, demand, start_date, end_date)
    data = CD.prep_data(data)
    
    return data

def train_model_tpot(data):
    """This function trains a model using the TPOT library
    :param data: The data to train the model on
    :return: The trained model"""

    X = data.drop(["Price"], axis=1)
    y = data["Price"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    print("Running TPOT model")
    model = TPOTRegressor(generations=2, population_size=50, verbosity=2, random_state=42)
    model.fit(X_train, y_train)
    print(model.score(X_test, y_test))
    tpot_pred = model.predict(X_test)

    mse = mean_squared_error(y_test, tpot_pred)
    r2 = r2_score(y_test, tpot_pred)
    print(f'TPOT Model mse: {mse}, r2: {r2}')
    model.export('models/scripts/tpot_price_pipeline.py')

    return model
def show_feature_importance(model, data):
    """This function shows the feature importance of the model, only if fitted pipline has the attribute 'feature_importances_'
    :param model: The trained model
    :param data: The data used to train the model"""
    fitted_pipeline = model.fitted_pipeline_
    final_estimator = fitted_pipeline.steps[-1][1]
    if hasattr(final_estimator, 'feature_importances_'):
        print(final_estimator.feature_importances_)
        feature_importance = model.feature_importances_
        feature_importance = 100.0 * (feature_importance / feature_importance.max())
        sorted_idx = np.argsort(feature_importance)
        pos = np.arange(sorted_idx.shape[0]) + .5
        plt.figure(figsize=(12, 6))
        plt.barh(pos, feature_importance[sorted_idx], align='center')
        plt.yticks(pos, data.columns[sorted_idx])
        plt.xlabel('Relative Importance')
        plt.title('Variable Importance')
        plt.show()
    else:
        print("The final estimator does not have an attribute 'feature_importances_'")
def main():
    data = get_data()
    tpot_model = train_model_tpot(data)
    #show_feature_importance(tpot_model, data)
    with open('models/models.pkl', 'r') as file:
        pickle.dump(tpot_model, file)
if __name__ == "__main__":
    main()