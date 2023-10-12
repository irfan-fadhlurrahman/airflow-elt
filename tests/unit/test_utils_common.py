import pandas as pd

from datetime import datetime, timedelta
from utils.common import (
    get_indonesia_time, get_minio_client, create_minio_bucket,
    write_dataframe_to_minio, MINIO_CREDENTIALS
)

def test_get_indonesia_time():
    """It assumed current machine timezone UTC+00:00"""
    assert get_indonesia_time().replace(microsecond=0) == (datetime.now() + timedelta(hours=7)).replace(microsecond=0)
    
def test_get_minio_client():
    print(get_minio_client())

def test_create_minio_bucket():
    create_minio_bucket(name='test')

def test_write_dataframe_to_minio():
    write_dataframe_to_minio(
        pd.read_parquet('tests/unit/files/2023-10-12 07_00_00_kualitas_udara.parquet'), 
        object_path="s3://test/air_quality/2023-10-12_07_00.parquet"
    )