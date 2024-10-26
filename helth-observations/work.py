import pprint
from datetime import datetime
from pathlib import Path
from data_loader import Loader
from plot import Plot

data_root = Path('./data')
plot_root = Path('plot-output')


data_file = data_root / 'observations.yaml'
loader = Loader(data_file=data_file)

data = loader.data()

pprint.pprint(data)


diastolic_series = []

for year, dates in data.items():
    for date_str, times in dates.items():
        for time_str, details in times.items():
            if details.get('type') == 'blood-pressure' and 'diastolic' in details:

                datetime_str = f"{year}-{date_str} {time_str}"
                timestamp = datetime.strptime(datetime_str, "%Y-%d-%m %H:%M")
                diastolic_value = details['diastolic']
                diastolic_series.append((timestamp, diastolic_value))

plot = Plot(diastolic_series, 'diastolic', plot_root)
