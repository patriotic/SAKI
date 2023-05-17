import pandas as pd

def transform_weather_data(df = pd.DataFrame):
    # Convert index into a column and reset index
    df = df.reset_index(names=['DATE', 'T2M', 'PRECTOTCORR', 'WS10M'])
    
    # Convert date column to datetime type
    df['DATE'] = pd.to_datetime(df['DATE'], format="%Y%m%d")
    
    return df
     

def transform_traffic_data(df = pd.DataFrame):
    # Convert date column to datetime type
    df['TATTAG'] = pd.to_datetime(df['TATTAG'], format="%d.%m.%Y")
    
    # Count number of traffic fine occurrences for each unique date
    date_counts = df.groupby('TATTAG')['TATTAG'].count()
    
    df = pd.DataFrame({'DATE':date_counts.index, 'FREQUENCIES':date_counts.values})
    
    return df
    
def merge_datasets(weather = pd.DataFrame, traffic = pd.DataFrame):
    merged_df = pd.merge(weather, traffic, on='DATE')
    print(merged_df)