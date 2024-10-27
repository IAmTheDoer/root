from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from matplotlib.patches import Rectangle
import numpy as np
import locale
from collections import defaultdict

locale.setlocale(locale.LC_TIME, 'da_DK')




class Plot:
    def __init__(self, data_series: list[tuple], title: str, x_type: str, y_type: str, destination: Path):
        data_series.sort()
        times, data_entries = zip(*data_series)

        mean_value = np.mean(data_entries)
        min_value = np.min(data_entries)
        max_value = np.max(data_entries)

        plt.figure(figsize=(10, 6))
        plt.plot(times, data_entries, marker='o', linestyle='-', linewidth=.5, markersize=2)

        # Plot mean, min, and max lines with labels
        plt.axhline(y=mean_value, color='r', linestyle='--', linewidth=.5, label=f'Mean: {mean_value:.0f}')
        plt.axhline(y=min_value, color='blue', linestyle=':', linewidth=.5, label=f'Min: {min_value:.0f}')
        plt.axhline(y=max_value, color='green', linestyle=':', linewidth=.5, label=f'Max: {max_value:.0f}')

        # Calculate and plot daily means
        daily_values = defaultdict(list)
        for time, value in zip(times, data_entries):
            daily_values[time.date()].append(value)

        daily_means = [(datetime.combine(day, datetime.min.time()) + timedelta(hours=12), np.mean(values))
                       for day, values in daily_values.items()]

        unique_dates = sorted(set(time.date() for time in times))

        daily_times, daily_mean_values = zip(*daily_means)
        plt.scatter(daily_times, daily_mean_values, color='purple', marker='D', s=20,
                    label=f'Daily Mean ({", ".join([f"{val:.0f}" for val in daily_mean_values])})')

        plt.title(title, pad=20)
        plt.xlabel(x_type)
        plt.ylabel(y_type)

        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%d-%m %H:%M"))
        plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=2))
        plt.xticks(times, rotation=45, ha="right", fontsize=6)
        plt.gcf().autofmt_xdate()
        plt.legend(fontsize=6, loc='upper left', bbox_to_anchor=(1, 1))

        # Flyt legend under grafen
        plt.legend(fontsize=6, loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)
        plt.subplots_adjust(bottom=0.20, top=0.90)

        locale.setlocale(locale.LC_TIME, 'en_US')

        # Add shifting color background per day and weekday label at 12:00
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

            # Add weekday name at 12:00 of each day's background
            midday = datetime.combine(day, datetime.min.time()) + timedelta(hours=12)
            weekday_name = day.strftime("%A")
            plt.text(
                mdates.date2num(midday),
                y_max,
                weekday_name,
                ha='center',
                va='bottom',
                fontsize=8,
                fontweight='bold',
                color='black'
            )

        destination.mkdir(exist_ok=True, parents=True)
        file_path = destination / f'{title}.png'
        plt.savefig(file_path, format='png', dpi=300)
        plt.close()
