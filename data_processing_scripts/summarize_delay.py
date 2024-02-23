import json
import os

import pandas as pd


def calculate_delay_percentage(df):
    total_buses = len(df)
    delayed_buses = len(df[df['Delay_minutes'] > 0])
    percentage = (delayed_buses / total_buses) * 100
    return percentage


def plot_delay():
    cwd = os.getcwd()
    dir = os.path.join(cwd, "filtered_data", "filt_bus_positions_busy.json")
    file = open(dir, "r")
    json_data = json.load(file)
    file.close()

    # Create dataframe:
    df = pd.DataFrame(json_data)

    # Convert to minutes:
    df['Delay_minutes'] = df['Time'] / 60

    # Group by district:
    grouped_data = df.groupby('District')
    for district, group in grouped_data:
        print(f"Nazwa dzielnicy: {district}")
        print("Spóźnienie:\tProcent:")
        for i in range(1, 6):  # Zakładam 5 kategorii spóźnień, dostosuj do swoich potrzeb
            subset = group[(group['Delay_minutes'] > (i - 1) * 5) & (group['Delay_minutes'] <= i * 5)]
            percentage = len(subset) / len(group) * 100 if len(group) > 0 else 0
            print(f"{i * 5 - 4}-{i * 5} min:\t\t{percentage:.2f}%")
        print("\n")

