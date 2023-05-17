import yaml
from pathlib import Path
import pandas as pd
from power_api import PowerAPI
import mobilithek
        
def get_weather_data():
    conf = get_config()
    latitude = conf.get('lat', 0)
    longitude = conf.get('lon', 0)
    start_date = conf.get('start_date', 0)
    end_date = conf.get('end_date', 0)
    param = conf.get('parameter')
    
    return PowerAPI(start=pd.Timestamp(str(start_date)), end=pd.Timestamp(str(end_date)), long=longitude, lat=latitude, parameter=param).get_data()

def save_weather_data():
    output_dir = get_output_path(get_config(), "weather_data.csv")
    df = get_weather_data()
    df.to_csv(output_dir, sep=";")

def get_traffic_data():
    return mobilithek.get_data()

def save_traffic_data():
    output_dir = get_output_path(get_config(), "traffic_data.csv")
    df = get_traffic_data()
    df.to_csv(output_dir, sep=";")

def get_config():
    config_file = './project/data/config.yaml'
    with open(config_file, 'rb') as f:
        return yaml.load(f, Loader=yaml.FullLoader)

def get_output_path(conf, filename: str):
    output_dir = conf.get('output_dir', 0)
    return Path(output_dir) / filename