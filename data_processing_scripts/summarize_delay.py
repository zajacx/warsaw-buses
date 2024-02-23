import json
import os
import pandas as pd
import matplotlib.pyplot as plt


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

    # Convert time to minutes:
    df['Delay_minutes'] = df['Time'] / 60
    grouped_data = df.groupby('District')

    # Prepare data for plots:
    categories = []
    percentages = []

    for i in range(1, 6):
        category = f"{i*5-4}-{i*5} min"
        categories.append(category)

        percentage_values = []
        for district, group in grouped_data:
            subset = group[(group['Delay_minutes'] > (i-1)*5) & (group['Delay_minutes'] <= i*5)]
            percentage = len(subset) / len(group) * 100 if len(group) > 0 else 0
            percentage_values.append(percentage)

        percentages.append(percentage_values)

    fig, ax = plt.subplots()

    for i, category in enumerate(categories):
        ax.bar([x + i*0.2 for x in range(len(grouped_data))], percentages[i], width=0.2, label=category)

    ax.set_xlabel('Dzielnica')
    ax.set_ylabel('Procent')
    ax.set_title('Procent spóźnionych autobusów w przedziałach czasowych')
    ax.set_xticks([x + 0.4 for x in range(len(grouped_data))])
    ax.set_xticklabels([district for district, _ in grouped_data], rotation='vertical')

    ax.legend()
    plt.show()

