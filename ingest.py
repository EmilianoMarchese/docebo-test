import logging
import os

import pandas as pd
import pymysql.err
import requests
from dotenv import load_dotenv
from sqlalchemy import create_engine

from models import Base
from settings import DATA_URL, TABLE_NAME

load_dotenv()


def get_logger(name):
    """
    Add a StreamHandler to a logger if still not added and
    return the logger
    :param name: str
    :return: logging.Stre
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.propagate = 1
        console = logging.StreamHandler()
        logger.addHandler(console)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console.setFormatter(formatter)
    return logger


def get_data(url):
    """
    Return a json-serialized object of the AirQuality data
    :param url: string
    :return: dict
    """
    json_data = {}
    try:
        response = requests.get(url)
        if response.status_code == 200:
            json_data = response.json()
    except Exception as e:
        main_logger.error(f'ERROR: Could not retrieve the data: {e}')
    return json_data


def create_df(json_data):
    """
    Return a dataframe with the AirQuality data
    :param json_data: dict
    :return: pd.DataFrame
    """
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
    main_logger = get_logger(__name__)
    main_logger.setLevel(logging.INFO)
    JSON_RAW_DATA = get_data(DATA_URL)
    out_df = create_df(JSON_RAW_DATA)
    MYSQL_URI = os.environ.get("MYSQL_URI")
    if not MYSQL_URI:
        raise Exception("ERROR: Provide a valid SQLDB URI")
    if not TABLE_NAME:
        raise Exception("ERROR: TABLE_NAME cannot be empty")
    db_ready = False
    main_logger.info("Connecting to MySQL DB")
    while not db_ready:
        try:
            engine = create_engine(MYSQL_URI)
            db_ready = True
        except pymysql.err.OperationalError:
            main_logger.warning("MYSQL not ready to accept connections, yet")
            continue
        except Exception as e:
            main_logger.error(f"{e}")
    Base.metadata.create_all(engine)
    main_logger.info("Structured created successfully")
    with engine.connect() as conn:
        out_df.to_sql(
            TABLE_NAME,
            index=False,
            con=conn,
            if_exists='append')
    main_logger.info(f"{len(out_df)} rows written to db")
