""" Run this script to update stored conditions, prices, and forecasts"""
from db_helpers import DB
import forecast as fc

if __name__ == '__main__':
    db = DB()
    db.update_curr_prices()
    db.update_curr_cond()
    fc.create_current_forecasts()