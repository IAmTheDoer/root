from pathlib import Path
import matplotlib.pyplot as plt


class Plot:
    def __init__(self, data_series: list[tuple], title: str, destination: Path):
        data_series.sort()
        times, diastolic_values = zip(*data_series)

        # Plot diastolic værdier mod tidspunkter
        plt.figure(figsize=(10, 6))
        plt.plot(times, diastolic_values, marker='o', linestyle='-')
        plt.title(f'{title} as function of time')
        plt.xlabel('time')
        plt.ylabel(title)
        plt.xticks(rotation=45, ha="right")
        plt.gcf().autofmt_xdate()  # Shortens date format for better readability

        # Gem plot som en fil
        file_path = destination / f'{destination}.png'
        destination.mkdir(exist_ok=True, parents=True)
        plt.savefig(file_path, format='png')
        plt.close()
