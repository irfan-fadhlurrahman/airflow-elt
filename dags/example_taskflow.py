import logging
from datetime import datetime, timedelta
from typing import Dict

import requests
from airflow.decorators import dag, task

import json
import pandas as pd
from typing import Dict, List
from utils.common import (
    get_indonesia_time, create_minio_bucket,
    write_dataframe_to_minio, query_using_duckdb
)

COMMON_DAG_ARGS = {
    "start_date": datetime.now() - timedelta(days=1),
    "catchup": False
}

@dag(schedule="*/15 * * * *", **COMMON_DAG_ARGS)
def klhk_air_quality():
    CURRENT_DATE = get_indonesia_time().strftime('%Y%m%d_%H%M')
    API = "https://ispu.menlhk.go.id/apimobile/v1/getStations"
    BUCKET_NAME = 'web-scraping'
    PREFIX_PATH = f's3://{BUCKET_NAME}/air_quality'
    DB_PATH = 'database/web-scraping.db'
    
    create_minio_bucket(BUCKET_NAME)
    
    @task(retries=2)
    def extract() -> List[Dict]:
        return requests.get(API).json()['rows']
        
    @task(multiple_outputs=True)
    def load(results: List[Dict]):
        write_dataframe_to_minio(
            df=pd.DataFrame(results),
            object_path=f"{PREFIX_PATH}/{CURRENT_DATE}.parquet"
        )
    
    @task(multiple_outputs=True)
    def transform():
        query_using_duckdb(
            db_path=DB_PATH,
            query=f"""
                CREATE OR REPLACE TABLE klhk_air_quality AS 
                FROM read_parquet (
                    '{PREFIX_PATH}/20231012_*.parquet'
                );
            """
        )
        print({
            "Total ROWS": query_using_duckdb(
                db_path=DB_PATH,
                query="SELECT COUNT(*) FROM klhk_air_quality"
            ).fetchall()
        })
    
    load(extract())
    transform()

klhk_air_quality()