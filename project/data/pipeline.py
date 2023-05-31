from extract import Extractor
from transform import Transformer
from load import Loader

class Pipeline:
    
    def __init__(self, extractor, transformer, loader) -> None:
        self.__extractor = extractor
        self.__transformer = transformer
        self.__loader = loader
    
    def run(self):
        # Extract weather data
        weather_data = self.__extractor.get_weather_data()
        
        # Extract traffic data
        traffic_data = self.__extractor.get_traffic_data()
        
        # Transform weather data
        transform_weather_data = self.__transformer.transform_weather_data(weather_data)
        
        # Transform traffic data
        transform_traffic_data = self.__transformer.transform_traffic_data(traffic_data)
        
        # Merge both transformed data
        merge_data = self.__transformer.merge_datasets(transform_weather_data, transform_traffic_data)
        
        # Load the data into SQLite database
        self.__loader.load_data_to_sqlite(merge_data)
            
if __name__ == "__main__":
    extractor = Extractor()
    transformer = Transformer()
    loader = Loader()
    pipeline = Pipeline(extractor, transformer, loader) 
    pipeline.run()