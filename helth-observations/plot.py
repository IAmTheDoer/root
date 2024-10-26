from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from matplotlib.patches import Rectangle
import numpy as np


class Plot:
    def __init__(self, data_series: list[tuple], title: str, destination: Path):
        data_series.sort()
        times, diastolic_values = zip(*data_series)

        mean_value = np.mean(diastolic_values)

        plt.figure(figsize=(10, 6))
        plt.plot(times, diastolic_values, marker='o', linestyle='-', linewidth=.5, markersize=2)
        plt.axhline(y=mean_value, color='r', linestyle='--', linewidth=1, label=f'Mean: {mean_value:.2f}')
        plt.title(f'{title} as function of time')
        plt.xlabel('Time')
        plt.ylabel(title)

        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%d-%m %H:%M"))
        plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=2))
        plt.xticks(times, rotation=45, ha="right", fontsize=3)
        plt.gcf().autofmt_xdate()
        plt.legend()

        # Add shifting color background per day
        unique_dates = sorted(set(time.date() for time in times))
        y_min, y_max = plt.ylim()
        for i, day in enumerate(unique_dates):
            color = "lightgrey" if i % 2 == 0 else "whitesmoke"
            plt.gca().add_patch(
                Rectangle(
                    (mdates.date2num(datetime.combine(day, datetime.min.time())), y_min),
                    mdates.date2num(datetime.combine(day + timedelta(days=1), datetime.min.time())) -
                    mdates.date2num(datetime.combine(day, datetime.min.time())),
                    y_max - y_min,
                    facecolor=color,
                    edgecolor="none",
                    zorder=0
                )
            )

        destination.mkdir(exist_ok=True, parents=True)
        file_path = destination / f'{title}.png'
        plt.savefig(file_path, format='png', dpi=300)
        plt.close()
