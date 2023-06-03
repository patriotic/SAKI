import pandas as pd
import sqlite3

# TrainstopsPipeline is responsible for creating ETL pipeline.
# It will extract the dataset (csv file) from the web, interprets and loads it into SQLite database.
class TrainstopsPipeline():
    # Datasource: https://mobilithek.info/offers/-8739430008147831066
    # Url for csv file.
    url = "https://download-data.deutschebahn.com/static/datasets/haltestellen/D_Bahnhof_2020_alle.CSV"
    def __init__(self) -> None:
        self.extractor = None
        self.transformer = None
        self.loader = None
    
    # Execute this method to run the pipeline.
    def run(self):
        # Create a extractor using csv file url.
        extractor = DataExtractor(self.url)
        
        # Create a tranformer using the extracted data. 
        transformer = DataTransformer(extractor.get_data_from_csv())
        
        # Create a loader using the transformed data.
        loader = DataLoader(transformer.transform())
        
        # Load the data into SQLite database.
        loader.load_data_to_sqlite()

# This class is responsible for fetching data from a url.
class DataExtractor():
    def __init__(self, url) -> None:
        self.url = url
    
    # Read a csv file and return a data frame object.
    def get_data_from_csv(self):
        if self.url:
            self.df = pd.read_csv(self.url, delimiter=";")
            return self.df

# This class is responsible for transforming the data.
class DataTransformer():
    def __init__(self, df= pd.DataFrame):
        self.df = df
    
    # Drop a single column
    def drop_single_column(self, column_name):
        self.df = self.df.drop(column_name, axis=1)
    
    # Filter rows with specific values in a column
    def filter_rows_with_values(self, column_name, values):
        self.df = self.df[self.df[column_name].isin(values)]
    
    # Replace a phrase in a column
    def replace_text(self, column_name, oldvalue, newvalue):
        self.df[column_name] = self.df[column_name].str.replace(oldvalue, newvalue)
    
    # Change the data types of columns 
    def change_data_types(self, data_types):
        self.df = self.df.astype(data_types)
    
    # Filter rows between first and last number
    def filter_rows_between_two_numbers(self,column_name, first_number, last_number):
        self.df = self.df[(self.df[column_name] < first_number) & (self.df[column_name] > last_number)]
    
    # Filter rows using a regex pattern
    def filter_rows_using_pattern(self, column_name, pattern):
        self.df = self.df[self.df[column_name].str.match(pattern)]
    
    # drop empty rows
    def drop_empty_rows(self):
        self.df = self.df.dropna()
    
    def transform(self):
        # Drop the 'Status' column.
        dropped_column = self.drop_single_column('Status')

        # Drop rows with empty cells
        self.drop_empty_rows()

        # Filter rows where 'Verkehr' column has 'FV', 'RV', 'nur DPN' values.
        self.filter_rows_with_values('Verkehr', ['FV', 'RV', 'nur DPN'])
        
        # Replace comma with period (decimal point) for 'Laenge' and 'Breite' 
        self.replace_text('Laenge', ',', '.')
        self.replace_text('Breite', ',', '.')

        # change the data types of the columns
        self.change_data_types({'EVA_NR': int, 'DS100': str, 'IFOPT': str, 'NAME': str, 
                                'Verkehr': str, 'Laenge': float, 'Breite': float, 
                                'Betreiber_Name': str, 'Betreiber_Nr': int})
        # Drop rows where 'Laenge' and 'Breite' values are beyond 90 and -90
        
        self.filter_rows_between_two_numbers('Laenge', 90,-90)
        self.filter_rows_between_two_numbers('Breite', 90,-90)
        
        # Filter the 'IFOPT' based on the pattern
        # <exactly two characters>:<any amount of numbers>:<any amount of numbers><optionally another colon followed by any amount of numbers>
        # ^: The caret symbol denotes the start of the string.
        # [A-Za-z]{2}: This pattern matches exactly two alphabetic characters. [A-Za-z] represents any uppercase or lowercase letter, and {2} specifies that we need exactly two of these characters.
        # :: Matches a colon character.
        # \d+: Represents one or more digits.
        # :: Matches a colon character.
        # \d+: Again, matches one or more digits.
        # (?::\d+)?: This is an optional group denoted by ?. It matches a colon character followed by one or more digits. The ?: inside the parentheses is a non-capturing group, which is used to group but not capture the matching portion.
        # $: The dollar sign denotes the end of the string.
        
        pattern = r'^[A-Za-z]{2}:\d+:\d+(?::\d+)?$'
        self.filter_rows_using_pattern('IFOPT', pattern)
        
        # Add the dropped column 'Status'
        self.df['Status'] = dropped_column
        
        return self.df

# This class is responsible for loading the data
class DataLoader():
    def __init__(self, df = pd.DataFrame):
        self.conn = None
        self.df = df
    
    # Create a connection, Load the data into SQLite database and close the connection
    def load_data_to_sqlite(self):
        self.connect_db()
        self.write_db()
        self.close_db()
        
    # Establish database connection
    def connect_db(self):
        self.conn = sqlite3.connect('./trainstops.sqlite')
        
    # Write the DataFrame to an SQLite table
    def write_db(self):
        if self.conn != None:
            self.df.to_sql(name='trainstops', con=self.conn, if_exists='replace')
    
    # Close the database connection
    def close_db(self):
        if self.conn != None:
            self.conn.close()

if __name__ == "__main__":
    # Create and execute the pipeline
    TrainstopsPipeline().run()