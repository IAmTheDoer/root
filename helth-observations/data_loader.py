from pathlib import Path
import yaml


class Loader:
    def __init__(self, data_file: Path):
        self._data_file = data_file
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
                            event.update(dict(zip(fields, event.pop("data"))))
        return self._data
