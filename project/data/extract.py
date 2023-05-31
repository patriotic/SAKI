import yaml
from pathlib import Path
import pandas as pd
from power_api import PowerAPIRemote
from mobilithek import MobilithekRemote
import os
        
class Extractor:
    def __init__(self) -> None:
        pass
    
    def get_weather_data(self):
        conf = self.get_config()
        latitude = conf.get('lat', 0)
        longitude = conf.get('lon', 0)
        start_date = conf.get('start_date', 0)
        end_date = conf.get('end_date', 0)
        param = conf.get('parameter')
        power_api_base_url = conf.get('power_api_base_url')
        
        return PowerAPIRemote(base_url= power_api_base_url,start=pd.Timestamp(str(start_date)), end=pd.Timestamp(str(end_date)), long=longitude, lat=latitude, parameter=param).get_data()

    def save_weather_data(self):
        output_dir = self.get_output_path(self.get_config(), "weather_data.csv")
        df = self.get_weather_data()
        df.to_csv(output_dir, sep=";")

    def get_traffic_data(self):
        conf = self.get_config()
        url = conf.get('traffic_data_base_url')
        return MobilithekRemote(url).get_data()

    def save_traffic_data(self):
        output_dir = self.get_output_path(self.get_config(), "traffic_data.csv")
        df = self.get_traffic_data()
        df.to_csv(output_dir, sep=";")

    def get_config(self):
        config_file = './project/data/config.yaml'
        with open(config_file, 'rb') as f:
            return yaml.load(f, Loader=yaml.FullLoader)

    def get_output_path(self, conf, filename: str):
        output_dir = conf.get('output_dir', 0)
        path = Path(output_dir)
        if not path.exists():
            os.makedirs(output_dir)
        return path / filename