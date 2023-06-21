from data.load import Loader
import pandas as pd

def test_if_data_loaded_to_SQLite():
    data = {
        'T2M': [2.5, 3.0, 2.0, 1.5],
        'PRECTOTCORR': [4.6, 5.2, 3.4, 4.5],
        'WS10M': [3.6, 4.2, 5.1, 2.8]
        }
    load_df = pd.DataFrame(data)
    loader = Loader('traffic_fines','project/data/data.sqlite')
    loader.load_data_to_sqlite(load_df)
    
    read_df = loader.read_data_from_sqlite()
    read_df = read_df.set_index(read_df.columns[0], drop=True)
    
    assert load_df.shape == read_df.shape