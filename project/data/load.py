import pandas as pd
import sqlite3

class Loader:
    def __init__(self, table_name, path):
        self.conn = None
        self.df = None
        self.table_name = table_name
        self.path = path
    
    def load_data_to_sqlite(self, df = pd.DataFrame):
        self.df = df
        self.connect_db()
        self.write_db()
        self.close_db()
        
    # Establish database connection
    def connect_db(self):
        self.conn = sqlite3.connect(self.path)
        
    # Write the DataFrame to an SQLite table
    def write_db(self):
        if self.conn != None:
            self.df.to_sql(name=self.table_name, con=self.conn, if_exists='replace')
    
    # Read the SQLite table
    def read_db(self):
        if self.conn != None:
            return pd.read_sql_table(self.table_name, 'sqlite:///' + self.path)
    
    # Close the database connection
    def close_db(self):
        if self.conn != None:
            self.conn.close()

    def read_data_from_sqlite(self):
        self.connect_db()
        df = self.read_db()
        self.close_db()
        return df