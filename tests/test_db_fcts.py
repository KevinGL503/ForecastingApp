from updater.db_helpers import DB
import pandas as pd

def test_get_table_as_df():
    db = DB()
    df = db.get_table_as_df('conditions')
    assert isinstance(df, pd.DataFrame)
    assert df.isna().sum().sum() == 0