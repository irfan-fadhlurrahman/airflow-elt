import pandas as pd

from datetime import datetime, timedelta
from utils.common import get_indonesia_time

def test_get_indonesia_time():
    """It assumed current machine timezone UTC+00:00"""
    assert get_indonesia_time().replace(microsecond=0) == (datetime.now() + timedelta(hours=7)).replace(microsecond=0)
    