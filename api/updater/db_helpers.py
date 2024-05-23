import day_conds as dc
import pandas as pd
import sqlite3
import os

def db_exists():
    """
    The function checks if a database file exists and creates it if it doesn't.
    :return: always returns `True`.
    """
    if not os.path.exists('api/updater/forecastDB.db'):
        con = sqlite3.connect('api/updater/forecastDB.db')
        print('Created DB file')
        return True
    return True

def make_new_table(name, columns):
    """
    The function `make_new_table` creates a new table in a SQLite database with the
    specified name and columns.
    
    :param name: name for the db table
    :param columns: columns in the table
    """
    db_exists()
    cols = ",".join(str(element) for element in columns)
    query = f"CREATE TABLE IF NOT EXISTS {name} ({cols})"
    con = sqlite3.connect('api/updater/forecastDB.db')
    cur = con.cursor()
    cur.execute(query)


def update_curr_cond():
    """
    The function `update_curr_cond` gets the current conditions and stores them
    in the database in a table called "conditions"
    """
    con = sqlite3.connect('api/updater/forecastDB.db')
    df = dc.get_today_cond()
    df.to_sql('conditions', con, index=True, index_label='TS', if_exists='replace')
