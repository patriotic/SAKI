from data.pipeline import Pipeline
from data.extract import Extractor
from data.transform import Transformer
from data.load import Loader
import os

def test_db_not_exists():
    path = "project/data/data.sqlite"
    if os.path.exists(path):
        os.remove(path)
    assert os.path.exists(path) == False
    
    
def test_run_pipeline():
    extractor = Extractor()
    transformer = Transformer()
    loader = Loader('traffic_fines','project/data/data.sqlite')
    pipeline = Pipeline(extractor, transformer, loader)
    pipeline.run()
    assert os.path.exists("./project/data/data.sqlite")