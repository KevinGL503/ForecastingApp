""" Run this script to update stored conditions, prices, and forecasts"""
from updater.db_helpers import DB
from updater import forecast as fc

def update():
    db = DB()
    db.update_curr_prices()
    db.update_curr_cond()
    fc.create_current_forecasts()