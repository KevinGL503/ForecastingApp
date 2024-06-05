from flask import Flask
from flask import render_template_string
from updater.db_helpers import DB
import json

api = Flask(__name__)

@api.route('/forecast/<zone>', methods=['GET'])
def forecasts(zone):
    db = DB()
    df = db.get_curr_forecast_json(zone)
    return df

@api.route('/conditions', methods=['GET'])
def conditions():
    db = DB()
    df = db.get_curr_conditions_json()
    return df

@api.route('/prices', methods=['GET'])
def prices():
    db = DB()
    df = db.get_curr_prices_json()
    return df

if __name__ == "__main__":
    api.run(debug=True, host='0.0.0.0',port=5555)