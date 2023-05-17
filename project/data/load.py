import pandas as pd
import sqlite3
import yaml

class LoadData:
    def __init__(self, df = pd.DataFrame):
        self.conn = None
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
            self.df.to_sql('traffic_fines', self.conn, if_exists='replace')
    
    # Close the database connection
    def close_db(self):
        if self.conn != None:
            self.conn.close()