import os.path
import pandas as pd
import matplotlib.pyplot as plt


def calculate_speed_percentage(df):
    total_rows = len(df)
    exceeding_speed_rows = len(df[df['speed'] > 50])
    percentage = (exceeding_speed_rows / total_rows) * 100
    return percentage


def plot_speed():
    # Load data from csv:
    cwd = os.getcwd()
    directory = os.path.join(cwd, "filtered_data", "filt_seg_busy.csv")
    file = pd.read_csv(directory)

    # Group data by districts and calculate speeding percentage:
    grouped_data = file.groupby('dist').apply(calculate_speed_percentage).reset_index(name='percentage')

    # Create dataframe with results:
    result_df = pd.DataFrame(grouped_data).rename(columns={'dist': 'Dzielnica', 'percentage': '% wykroczeń'})

    # Plotting the results:
    result_df.plot(kind='bar', x='Dzielnica', y='% wykroczeń', legend=False)
    plt.xlabel('Dzielnica')
    plt.ylabel('% wykroczeń')
    plt.title('Procent autobusów przekraczających prędkość w poszczególnych dzielnicach')
    plt.show()

    # print(result_df)
    print("\n")
