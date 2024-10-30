from pathlib import Path
import yaml
from statistics import mean


class Loader:
    def __init__(self, data_file: Path):
        self._data_file = data_file
        self._verbose = True
        if not data_file.exists():
            print(f'{data_file} not found in this working directory("{Path.cwd()}").')
            self._data = {}
        else:
            with open(data_file, 'r') as file:
                self._data = yaml.safe_load(file)

    def data(self) -> dict:
        data_format = self._data.pop('data_format')

        for year, dates in self._data.items():
            for date, times in dates.items():
                for time, event in times.items():
                    event_type = event.get("type")
                    if event_type in data_format:
                        fields = data_format[event_type].split(", ")
                        if "data" in event and len(event["data"]) == len(fields):
                            self._print(f'event_type= {event_type}, fields= {fields}, data= {event["data"]}')
                            if all(isinstance(x, (int, float)) for x in event['data']):
                                event.update(dict(zip(fields, event.pop("data"))))
                            elif all(isinstance(x, list) for x in event['data']):
                                mean_values = [round(mean(sublist)) for sublist in event.pop('data')]
                                event.update(dict(zip(fields, mean_values)))
                            else:
                                raise ValueError(f'Problem with {event["data"]}')
        return self._data

    def _print(self, info):
        if self._verbose:
            print(f'{info}')
