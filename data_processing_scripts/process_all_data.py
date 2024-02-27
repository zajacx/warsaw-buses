from data_processing_scripts.prepare_speed_stats import prepare_speed_stats
from data_processing_scripts.prepare_pos_stats import prepare_pos_stats
from data_processing_scripts.summarize_speed import plot_speed
from data_processing_scripts.summarize_delay import plot_delay


def process_all_data():
    # prepare_speed_stats()
    # prepare_pos_stats()
    plot_speed()
    plot_delay()
