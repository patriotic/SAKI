import extract
import transform
from load import LoadData

def get_weather_data():
    return extract.get_weather_data()

def transform_weather_data():
    return transform.transform_weather_data(get_weather_data())

def get_traffic_data():
    return extract.get_traffic_data()

def transform_traffic_data():
    return transform.transform_traffic_data(get_traffic_data())

def merge_data():
    return transform.merge_datasets(
        transform_weather_data(),
        transform_traffic_data()
        )
    
def load_data_into_sqlite():
    LoadData(merge_data())

if __name__ == "__main__":
    load_data_into_sqlite()