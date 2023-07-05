import pandas as pd
import sqlite3
import urllib.request as req
import zipfile
import os

# TemperaturesPipeline is responsible for creating ETL pipeline.
# It will extract the dataset (csv file) from the web, interprets and loads it into SQLite database.
class TemperaturesPipeline():
    # Datasource: https://mobilithek.info/offers/526718847762190336
    source_url = "https://www.mowesta.com/data/measure/mowesta-dataset-20221107.zip"
    directory = "./exercises/" 
    zip_filename = "mowesta.zip"
    csv_filename = "data.csv"
    db_filename = "temperatures.sqlite"
    db_tablename = "temperatures"
    columns = ["Geraet", "Hersteller", "Model", "Monat", "Temperatur in °C (DWD)", "Batterietemperatur in °C", "Geraet aktiv"]
    
    def __init__(self) -> None:
        self.extractor = None
        self.transformer = None
        self.loader = None
    
    # Execute this method to run the pipeline.
    def run(self):
        # Create a extractor using csv file url.
        extractor = DataExtractor(self.source_url, self.directory, self.zip_filename, self.csv_filename)
        
        # Create a tranformer using the extracted data. 
        transformer = DataTransformer(extractor.get_data_from_csv(self.columns))
        
        # Create a loader
        loader = DataLoader(self.directory, self.db_filename, self.db_tablename)
        
        # Load the data into SQLite database.
        loader.load_data_to_sqlite(transformer.transform())

# This class is responsible for fetching data from a url.
class DataExtractor():
    def __init__(self, source, directory, zip_filename, csv_filename) -> None:
        self.source = source
        self.directory = directory
        self.zip_filename = zip_filename
        self.csv_filename = csv_filename
        self.run()
        
    def run(self):
        self.download_zip_file()
        self.extract_data_from_zip()
    
    def zip_file_path(self):
        return os.path.join(self.directory, self.zip_filename)
    
    def csv_file_path(self):
        return os.path.join(self.directory, self.csv_filename)
    
    def download_zip_file(self):
        req.urlretrieve(self.source, self.zip_file_path())
    
    def extract_data_from_zip(self):
        with zipfile.ZipFile(self.zip_file_path(), 'r') as zip_ref:
            zip_ref.extract(self.csv_filename, self.directory)
            
    # Read a csv file and return a data frame object.
    def get_data_from_csv(self, columns):
        if self.csv_file_path():
            self.df = pd.read_csv(self.csv_file_path(), sep=";", decimal=",", usecols=columns, index_col=False)
            return self.df

# This class is responsible for transforming the data.
class DataTransformer():
    def __init__(self, df= pd.DataFrame):
        self.df = df
    
    def transform(self):
        # Rename columns
        columns = { "Temperatur in °C (DWD)" : "Temperatur", "Batterietemperatur in °C" : "Batterietemperatur" }
        self.df = self.df.rename(columns= columns)
        
        # Convert Celsius to Fahrenheit
        self.df['Temperatur'] = (self.df['Temperatur'] * 9/5) + 32
        self.df['Batterietemperatur'] = (self.df['Batterietemperatur'] * 9/5) + 32
        
        # Validation
        self.df['Geraet'] = self.df['Geraet'] > 0
        self.df = self.df[(self.df['Monat'] > 0) & (self.df['Monat'] < 13)]
        
        return self.df

# This class is responsible for loading the data
class DataLoader():
    def __init__(self, directory, file_name, table_name):
        self.conn = None
        self.directory = directory
        self.file_name = file_name
        self.table_name = table_name
    
    # Create a connection, Load the data into SQLite database and close the connection
    def load_data_to_sqlite(self,  df = pd.DataFrame):
        self.df = df
        self.connect_db()
        self.write_db()
        self.close_db()
    
    def db_file_path(self):
        return os.path.join(self.directory, self.file_name)
    
    # Establish database connection
    def connect_db(self):
        self.conn = sqlite3.connect(self.db_file_path())
        
    # Write the DataFrame to an SQLite table
    def write_db(self):
        if self.conn != None:
            self.df.to_sql(name=self.table_name, con=self.conn, if_exists='replace', index= False)
    
    # Read the SQLite table
    def read_db(self):
        if self.conn != None:
            return pd.read_sql_table(self.table_name, 'sqlite:///' + self.db_file_path())
    
    # Close the database connection
    def close_db(self):
        if self.conn != None:
            self.conn.close()
                
                
if __name__ == "__main__":
    # Create and execute the pipeline
    TemperaturesPipeline().run()