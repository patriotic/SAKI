import pandas as pd

url = "https://opendata.bonn.de/sites/default/files/GeschwindigkeitsverstoesseBonn2020.csv"

def get_data():
    return pd.read_csv(url, delimiter=";")