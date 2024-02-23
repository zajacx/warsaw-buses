import os.path

import pandas as pd


def calculate_speed_percentage(df):
    total_rows = len(df)
    exceeding_speed_rows = len(df[df['speed'] > 50])
    percentage = (exceeding_speed_rows / total_rows) * 100
    return percentage


def plot_speed():
    # Load data from csv:
    cwd = os.getcwd()
    dir = os.path.join(cwd, "filtered_data", "filt_seg_busy.csv")
    file = pd.read_csv(dir)

    # Group data by districts and calculate speeding percentage:
    grouped_data = file.groupby('dist1').apply(calculate_speed_percentage).reset_index(name='percentage')

    # Create dataframe with results:
    result_df = pd.DataFrame(grouped_data).rename(columns={'dist1': 'Dzielnica', 'percentage': '% wykroczeń'})
    print(result_df)
    print("\n")
