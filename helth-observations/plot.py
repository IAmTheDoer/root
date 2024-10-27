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
    def __init__(self, data_series: list[list[tuple]], title: str, x_type: str, y_type: str, destination: Path, events: list[tuple] = None, series_labels: list[str] = None):
        plt.figure(figsize=(10, 6))

        # Plot each data series
        for idx, series in enumerate(data_series):
            series.sort()
            times, data_entries = zip(*series)
            label = series_labels[idx] if series_labels and idx < len(series_labels) else f'Series {idx + 1}'

            # Plot the individual series
            plt.plot(times, data_entries, marker='o', linestyle='-', linewidth=.5, markersize=2, label=label)

            # Calculate mean, min, max for each series and add lines
            mean_value = np.mean(data_entries)
            min_value = np.min(data_entries)
            max_value = np.max(data_entries)
            plt.axhline(y=mean_value, color='red', linestyle='--', linewidth=.5, label=f'{label} Mean: {mean_value:.0f}')
            plt.axhline(y=min_value, color='blue', linestyle=':', linewidth=.5, label=f'{label} Min: {min_value:.0f}')
            plt.axhline(y=max_value, color='green', linestyle=':', linewidth=.5, label=f'{label} Max: {max_value:.0f}')

            # Calculate daily means and plot them as points
            daily_values = defaultdict(list)
            for time, value in zip(times, data_entries):
                daily_values[time.date()].append(value)

            daily_means = [(datetime.combine(day, datetime.min.time()) + timedelta(hours=12), np.mean(values))
                           for day, values in daily_values.items()]

            if daily_means:
                daily_times, daily_mean_values = zip(*daily_means)
                plt.scatter(daily_times, daily_mean_values, color='purple', marker='D', s=20, label=f'{label} Daily Mean')

        plt.title(title, pad=20)
        plt.xlabel(x_type)
        plt.ylabel(y_type)

        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%d-%m %H:%M"))
        plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=6))
        plt.xticks(rotation=45, ha="right", fontsize=6)
        plt.gcf().autofmt_xdate()

        # Place legend below the plot
        plt.legend(fontsize=6, loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)
        plt.subplots_adjust(bottom=0.25, top=0.90)

        # Add background color per day and weekday label at 12:00
        unique_dates = sorted(set(time.date() for series in data_series for time, _ in series))
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

        # Plot events if provided
        if events:
            for event_time, description in events:
                plt.axvline(x=event_time, color='orange', linestyle='--', linewidth=0.8)
                plt.text(event_time, y_min + 1, description, rotation=90, va='bottom', ha='right', fontsize=6, color='orange')

        destination.mkdir(exist_ok=True, parents=True)
        file_path = destination / f'{title}.png'
        plt.savefig(file_path, format='png', dpi=300)
        plt.close()
