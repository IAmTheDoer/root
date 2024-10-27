import pprint
from datetime import datetime
from pathlib import Path
from data_loader import Loader
from plot import Plot
from report import Report


data_root = Path('./data')
plot_root = Path('[plot-output]')

the_data_file = 'week-43'

data_file = data_root / f'{the_data_file}.yaml'
loader = Loader(data_file=data_file)

data = loader.data()

pprint.pprint(data)


def create_plots(data, scope: str):
    diastolic_series = []
    systolic_series =[]
    heart_rate_series = []
    exercise_series = []

    for year, dates in data.items():
        for date_str, times in dates.items():
            for time_str, details in times.items():
                datetime_str = f"{year}-{date_str} {time_str}"
                timestamp = datetime.strptime(datetime_str, "%Y-%d-%m %H:%M")
                if details.get('type') == 'blood-pressure':
                    if 'systolic' in details:
                        systolic_value = details['systolic']
                        systolic_series.append((timestamp, systolic_value))
                    if 'diastolic' in details:
                        diastolic_value = details['diastolic']
                        diastolic_series.append((timestamp, diastolic_value))
                    if 'heart_rate' in details:
                        heart_rate_value = details['heart_rate']
                        heart_rate_series.append((timestamp, heart_rate_value))
                elif details.get('type') == 'exercise':
                    if 'exercise' in details:
                        exercise = details['exercise']
                        exercise_series.append((timestamp, exercise))

    Plot(diastolic_series, f'diastolic pressure {scope}', x_type='time', y_type='mmHg', destination=plot_root)
    Plot(systolic_series, f'systolic pressure {scope}', x_type='time', y_type='mmHg', destination=plot_root)
    Plot(heart_rate_series, f'heart rate {scope}', x_type='time', y_type='/min', destination=plot_root)


def create_data_report(data, scope: str):
    rows = []
    index = 0
    for year, dates in data.items():
        for date_str, times in dates.items():
            for time_str, details in times.items():
                datetime_str = f"{year}-{date_str} {time_str}"
                timestamp = datetime.strptime(datetime_str, "%Y-%d-%m %H:%M")
                if details.get('type') == 'blood-pressure':
                    rows.append((timestamp, f'[{index:3}] {timestamp} => blood pressure: {details['systolic']:3}/{details['diastolic']:3} - {details['heart_rate']:3} note: {details['note']}\n'))
                elif details.get('type') == 'exercise':
                    rows.append((timestamp, f'[{index:3}] {timestamp} => exercise      : {details['exercise']} - {details['note']}\n'))
                index += 1

    Report(rows, f'data report {the_data_file}', destination=plot_root)


create_plots(data, the_data_file)
create_data_report(data, the_data_file)