import pprint
from datetime import datetime
from pathlib import Path
from data_loader import Loader
from plot import Plot

data_root = Path('./data')
plot_root = Path('[plot-output]')


data_file = data_root / 'observations.yaml'
loader = Loader(data_file=data_file)

data = loader.data()

pprint.pprint(data)


diastolic_series = []
systolic_series =[]
heart_rate_series = []

for year, dates in data.items():
    for date_str, times in dates.items():
        for time_str, details in times.items():
            if details.get('type') == 'blood-pressure':
                datetime_str = f"{year}-{date_str} {time_str}"
                timestamp = datetime.strptime(datetime_str, "%Y-%d-%m %H:%M")
                if 'diastolic' in details:
                    diastolic_value = details['diastolic']
                    diastolic_series.append((timestamp, diastolic_value))
                if 'systolic' in details:
                    systolic_value = details['systolic']
                    systolic_series.append((timestamp, systolic_value))
                if 'heart_rate' in details:
                    heart_rate_value = details['heart_rate']
                    heart_rate_series.append((timestamp, heart_rate_value))

plot = Plot(diastolic_series, 'diastolic pressure', x_type='time', y_type='mmHg', destination=plot_root)
plot = Plot(systolic_series, 'systolic pressure', x_type='time', y_type='mmHg', destination=plot_root)
plot = Plot(heart_rate_series, 'heart rate', x_type='time', y_type='/min', destination=plot_root)
