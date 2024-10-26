from pathlib import Path
from data_loader import Loader

data_file = Path() / 'observations.yaml'

loader = Loader(data_file=data_file)

data = loader.data(data_file)

print(data)