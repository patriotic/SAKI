from typing import List, Union, Optional
from pathlib import Path
from datetime import date, datetime
import requests
import pandas as pd

class PowerAPI:
    url =  "https://power.larc.nasa.gov/api/temporal/daily/point?"
    def __init__(self,
                 start: Union[date, datetime, pd.Timestamp],
                 end: Union[date, datetime, pd.Timestamp],
                 long: float, lat: float,
                 use_long_names: bool = False,
                 parameter: Optional[List[str]] = None):
        self.start = start
        self.end = end
        self.long = long
        self.lat = lat
        self.use_long_names = use_long_names
        self.parameter = parameter

        self.request = self._build_request()

    def _build_request(self):
        r = self.url
        r += f"parameters={(',').join(self.parameter)}"
        r += '&community=RE'
        r += f"&longitude={self.long}"
        r += f"&latitude={self.lat}"
        r += f"&start={self.start.strftime('%Y%m%d')}"
        r += f"&end={self.end.strftime('%Y%m%d')}"
        r += '&format=JSON'

        return r

    def get_data(self):
        response = requests.get(self.request)

        assert response.status_code == 200

        data_json = response.json()

        records = data_json['properties']['parameter']

        df = pd.DataFrame.from_dict(records)

        return df