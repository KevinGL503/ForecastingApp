from flask import Flask
from flask import render_template_string
from updater.db_helpers import DB
import json

def init_api(server):
    @server.route('/api/forecast/<zone>', methods=['GET'])
    def forecasts(zone):
        db = DB()
        df = db.get_curr_forecast_json(zone)
        return df

    @server.route('/api/conditions', methods=['GET'])
    def conditions():
        db = DB()
        df = db.get_curr_conditions_json()
        return df

    @server.route('/api/prices', methods=['GET'])
    def prices():
        db = DB()
        df = db.get_curr_prices_json()
        return df
