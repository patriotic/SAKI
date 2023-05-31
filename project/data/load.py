import pandas as pd
import sqlite3

class Loader:
    def __init__(self):
        self.conn = None
        self.df = None
    
    def load_data_to_sqlite(self, df = pd.DataFrame):
        self.df = df
        self.connect_db()
        self.write_db()
        self.close_db()
        
    # Establish database connection
    def connect_db(self):
        self.conn = sqlite3.connect('./project/data/data.sqlite')
        
    # Write the DataFrame to an SQLite table
    def write_db(self):
        if self.conn != None:
            self.df.to_sql(name='traffic_fines', con=self.conn, if_exists='replace')
    
    # Close the database connection
    def close_db(self):
        if self.conn != None:
            self.conn.close()