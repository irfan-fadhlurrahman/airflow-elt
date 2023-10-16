from dataclasses import dataclass
from minio import Minio, api

@dataclass
class MinioCredentials:
    key: str = os.environ.get('MINIO_ROOT_USER'),
    secret: str = os.environ.get('MINIO_ROOT_PASSWORD'),
    host: str = os.environ.get('MINIO_HOST'),
    port: int = os.environ.get('MINIO_PORT'),
    endpoint: str = os.environ.get('MINIO_ENDPOINT'),

class MinioFileHandler:
    def __init__(self, , bucket_name: str, credentials: MinioCredentials = MinioCredentials()):
        self.key = credentials.key
        self.secret = credentials.secret
        self.host = credentials.host
        self.port = credentials.port
        self.endpoint = credentials.endpoint
        self.bucket_name = bucket_name
        self.prefix_path = f"s3://{self.bucket_name}"
        self.use_ssl = False
        self.client = None
        self.create_bucket(self.bucket_name)
    
    def get_client(self) -> api.Minio:
        """Temporarily use insecure connection to interact with Minio S3 API"""
        self.client = Minio(
            f"{self.host}:{self.port}",
            access_key=self.key,
            secret_key=self.secret,
            secure=False,
            cert_check=False
        )
        return self.client
        
    def create_bucket(self, name: str):
        if self.client is None:
            self.client = self.get_client()
        
        if not self.client.bucket_exists(name):
            self.client.make_bucket(name)
            print(f"Created Bucket '{name}'")
    
    def write_dataframe_as_parquet(self, df: pd.DataFrame, object_path: str):
        if not object_path.endswith('.parquet'):
            print('Currently only accepts parquet file')
            return None

        df.to_parquet(
            object_path=f"{self.prefix_path}/{object_path}", 
            storage_options={
                "key": self.key,
                "secret": self.secret,
                "client_kwargs": {"endpoint_url": self.endpoint},
                "use_ssl": False
        })
        print(f"Save to Minio Object Storage at {object_path}")