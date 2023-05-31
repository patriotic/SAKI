from data.extract import Extractor
import os
import pytest

@pytest.fixture
def extractor():
    return Extractor()

def test_if_weather_data_is_extracted(extractor):
    extractor.save_weather_data()
    
    assert os.path.exists("./project/data/extras/weather_data.csv")
    
def test_if_traffic_data_is_extracted(extractor):
    extractor.save_traffic_data()
    
    assert os.path.exists("./project/data/extras/traffic_data.csv")