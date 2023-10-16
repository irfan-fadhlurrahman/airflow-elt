import pandas
import duckdb

from utils.common import get_indonesia_time
from utils.file_handler import MinioFileHandler

class KLHKAirQuality:
    def __init__(self, file_handler: MinioFileHandler):
        self.current_date = get_indonesia_time().strftime('%Y%m%d_%H%M')
        self.file_handler = file_handler
        self.bucket_name = 'web-scraping'
        self.db_path = "database/web-scraping.db"
        self.api_url = "https://ispu.menlhk.go.id/apimobile/v1/getStations"
    
    def extract(self) -> List[Dict]:
        return requests.get(api_url).json()['rows']
    
    def load(results: List[Dict]):
        self.file_handler(bucket_name=self.bucket_name) \
            .write_dataframe_as_parquet(
                df=pd.DataFrame(results),
                object_path=f"air_quality/{self.current_date}.parquet"
            )
    
    def transform():
        con = duckdb.connect(self.db_path)
        con.sql(f"""
            CREATE OR REPLACE TABLE klhk_air_quality AS
            FROM read_parquet ('s3://{}/air_quality/*.parquet');
        """)