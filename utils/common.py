import os
import pytz
import pandas as pd

from minio import api
from datetime import datetime
from dotenv import load_dotenv

from utils.file_handler import MinioCredentials, MinioFileHandler

load_dotenv()

MINIO_CREDENTIALS = MinioCredentials(
    key=os.environ.get('MINIO_ROOT_USER'),
    secret=os.environ.get('MINIO_ROOT_PASSWORD'),
    host=os.environ.get('MINIO_HOST'),
    port=os.environ.get('MINIO_PORT'),
    endpoint=os.environ.get('MINIO_ENDPOINT'),
)

def get_indonesia_time() -> datetime:
    """To ensure the datetime is UTC+07:00 and without tzinfo"""
    return datetime.now(tz=pytz.timezone('Asia/Jakarta')).replace(tzinfo=None)

def get_minio_client() -> api.Minio:
    return MinioFileHandler(credentials=MINIO_CREDENTIALS).get_client()

def create_minio_bucket(name: str):
    return MinioFileHandler(credentials=MINIO_CREDENTIALS).create_bucket(name)

def write_dataframe_to_minio(df: pd.DataFrame, object_path: str):
    if not object_path.endswith('.parquet'):
        print('Currently only accepts parquet file')
        return None
    
    df.to_parquet(object_path, storage_options={
        "key": MINIO_CREDENTIALS.key,
        "secret": MINIO_CREDENTIALS.secret,
        "client_kwargs": {"endpoint_url": MINIO_CREDENTIALS.endpoint},
        "use_ssl": False
    })
    print(f"Save to Minio Object Storage at {object_path}")
    