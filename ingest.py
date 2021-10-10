import os

import pandas as pd
import requests
from dotenv import load_dotenv
from sqlalchemy import create_engine
from settings import DATA_URL, TABLE_NAME

load_dotenv()


def get_data(url):
    json_data = {}
    try:
        response = requests.get(url)
        if response.status_code == 200:
            json_data = response.json()
    except Exception as e:
        print(f'ERROR: Could not retrieve the data: {e}')
    return json_data


def create_df(json_data):
    if not json_data:
        raise Exception('ERROR: trying to parse empty json data')
    columns, columns_to_drop = [], []
    for c in json_data['meta']['view']['columns']:
        columns.append(c['name'])
        if c['id'] == -1:
            columns_to_drop.append(c['name'])
    df = pd.DataFrame(json_data['data'], columns=columns)
    df.drop(columns=columns_to_drop, inplace=True)
    df.dropna(inplace=True)
    return df


if __name__ == '__main__':
    JSON_RAW_DATA = get_data(DATA_URL)
    out_df = create_df(JSON_RAW_DATA)
    MYSQL_URI = os.environ.get("MYSQL_URI")
    if not MYSQL_URI:
        raise Exception("ERROR: Provide a valid SQLDB URI")
    if not TABLE_NAME:
        raise Exception("ERROR: TABLE_NAME cannot be empty")
    engine = create_engine(MYSQL_URI)
    with engine.connect() as conn:
        conn.execute(f'TRUNCATE TABLE `{TABLE_NAME}`')
        out_df.to_sql(TABLE_NAME, index=False, con=conn, if_exists='append')
    print(f"DONE! {len(out_df)} rows written to db")
