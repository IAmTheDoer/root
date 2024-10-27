from pathlib import Path


class Report:
    def __init__(self, data_series: list[tuple], title: str, destination: Path):
        data_series.sort()
        times, data_entries = zip(*data_series)

        file_path = destination / f'{title}.txt'

        with open(file_path, 'w', encoding='utf-8') as file_:
            file_.write(f'***** {title}\n\n')
            file_.writelines(data_entries)
