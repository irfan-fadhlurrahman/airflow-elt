import pandas as pd

from datetime import datetime, timedelta
from utils.common import (
    get_indonesia_time, get_minio_client, create_minio_bucket,
    write_dataframe_to_minio, MINIO_CREDENTIALS, query_using_duckdb
)

def __test_get_indonesia_time():
    """It assumed current machine timezone UTC+00:00"""
    assert get_indonesia_time().replace(microsecond=0) == (datetime.now() + timedelta(hours=7)).replace(microsecond=0)
    
def __test_get_minio_client():
    print(get_minio_client())

def __test_create_minio_bucket():
    create_minio_bucket(name='test')

def __test_write_dataframe_to_minio():
    write_dataframe_to_minio(
        pd.read_parquet('tests/files/2023-10-12 07_00_00_kualitas_udara.parquet'), 
        object_path="s3://test/air_quality/2023-10-12_07_00.parquet"
    )

def __test_query_from_duckdb_insert():
    db_path = 'database/web-scraping.db'
    query = f"""
        CREATE TABLE IF NOT EXISTS user_info(
            name TEXT,
            description TEXT,
            user_id TEXT PRIMARY KEY
        );
        INSERT INTO user_info (name, description, user_id)
        VALUES ('Irfan Fadhlurrahman', 'Data Engineer', '269037');
        SELECT * FROM user_info;
    """
    assert query_using_duckdb(db_path, query).fetchall() == [('Irfan Fadhlurrahman', 'Data Engineer', '269037')]
    
    query_using_duckdb(
        db_path, 
        query="DELETE FROM user_info;"
    )
    
def __test_query_from_duckdb_replace():
    query_using_duckdb(
        db_path='database/web-scraping.db',
        query=f"""
            CREATE OR REPLACE TABLE klhk_air_quality AS FROM read_parquet (
                tests/files/2023-10-12 07_00_00_kualitas_udara.parquet
            );
        """
        )
    results = query_using_duckdb(
        db_path='database/web-scraping.db',
        query=f"SELECT COUNT(*) FROM klhk_air_quality"
    )
    print(results.fetchall())
    