import csv
from datetime import datetime

import matplotlib.pyplot as plt

filename_dv = 'data/death_valley_2018_simple.csv'
filename_sit = 'data/sitka_weather_2018_simple.csv'
with open(filename_sit) as sit, open(filename_dv) as dv:
    reader_sit = csv.reader(sit)
    header_row_sit = next(reader_sit)
    reader_dv = csv.reader(dv)
    header_row_dv = next(reader_dv)

    # for index, column_header in enumerate(header_row):
    #     print(index, column_header)

    # Get dates, high and low temperatures from this file
    dates, highs_s, lows_s = [], [], []
    highs_d, lows_d = [], []

    # Reading Death Valley file
    for row in reader_dv:
        current_date = datetime.strptime(row[2], '%Y-%m-%d')
        try:
            high = int(row[4])
            low = int(row[5])
        except ValueError:
            print(f"Missing data for {current_date}")
        else:
            highs_d.append(high)
            lows_d.append(low)

    # Reading Sitka file
    for row in reader_sit:
        current_date = datetime.strptime(row[2], '%Y-%m-%d')
        try:
            high = int(row[5])
            low = int(row[6])
        except ValueError:
            print(f"Missing data for {current_date}")
        else:
            dates.append(current_date)
            highs_s.append(high)
            lows_s.append(low)
# print(highs)

    # Plot the high and low temperatures
    plt.style.use('seaborn')
    fig, ax = plt.subplots()
    ax.plot(dates, highs_s, c='red', alpha=0.4)
    ax.plot(dates, lows_s, c='blue', alpha=0.4)
    ax.plot(dates, highs_d, c='red', alpha=0.4)
    ax.plot(dates, lows_d, c='blue', alpha=0.4)
    ax.fill_between(dates, highs_s, highs_d, facecolor='red', alpha=0.1)
    ax.fill_between(dates, lows_s, lows_d, facecolor='blue', alpha=0.1)

    # Format plot
    title = "Daily high and low temperatures comparison - 2018\nDeath Valley, CA and Sitka"
    ax.set_title(title, fontsize = 20)
    ax.set_xlabel('', fontsize = 16)
    fig.autofmt_xdate()
    ax.set_ylabel("Temperature (F)", fontsize=16)
    ax.tick_params(axis='both', which='major', labelsize=16)

    plt.show()

