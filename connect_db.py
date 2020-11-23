import sqlite3
import pandas as pd


DB_PATH = r"C:\projects\final\events_alert_app\events_alert_app\webapp.db"


def execute_query(query: str, db_path: str) -> pd.DataFrame:
    with sqlite3.connect(db_path) as connect:
        return pd.read_sql(query, connect)

_sql = "select id, description from event"
_description_df = execute_query(_sql, DB_PATH)
assert "description" in _description_df.columns


def get_data_from_db_by_search(search_request: str) -> dict:
    _filter_df = lambda row: search_request.lower() in row["description"].lower()
    description_df = _description_df[_description_df.apply(_filter_df, axis=1)]  # subset подмножество df
    ids_you_are_looking_for = list(map(str, description_df['id']))
    ids_str = ",".join(ids_you_are_looking_for)  # df into list
    sql_for_search = f"select * from event where id in ({ ids_str })"
    return execute_query(sql_for_search, DB_PATH)
