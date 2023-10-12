from dataclasses import dataclass
from minio import Minio, api


@dataclass
class MinioCredentials:
    key: str
    secret: str
    host: str
    port: int
    endpoint: str
    

class MinioFileHandler:
    def __init__(self, credentials: MinioCredentials):
        self.key = credentials.key
        self.secret = credentials.secret
        self.host = credentials.host
        self.port = credentials.port
        self.endpoint = credentials.endpoint
        self.use_ssl = False
        self.client = None
    
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
        
        if self.client.bucket_exists(name):
            print(f"Bucket '{name}' exists.")
        else:
            self.client.make_bucket(name)
            print(f"Created Bucket '{name}'")