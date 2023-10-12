import duckdb
import traceback

from contextlib import contextmanager
from dotenv import load_dotenv

from utils.file_handler import MinioCredentials

load_dotenv()

class DuckDBConnection:
    def __init__(self, db_path: str, credentials: MinioCredentials):
        """"""
        self.db_path = db_path
        self.key = credentials.key
        self.secret = credentials.secret
        self.host = credentials.host
        self.port = credentials.port
    
    def execute(self, query: str) -> duckdb.DuckDBPyConnection:
        conn = duckdb.connect(self.db_path, read_only=False)
        return conn.execute(f"""
            INSTALL httpfs;
            LOAD httpfs;
            SET s3_use_ssl=false;
            SET s3_url_style='path';
            SET s3_access_key_id='{self.key}';
            SET s3_secret_access_key='{self.secret}';
            SET s3_endpoint='{self.host}:{self.port}';
            {query}
        """)