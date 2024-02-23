import os

from data_collectors.dict_collector import get_dict
from data_collectors.bus_stops_collector import get_bus_stops
from data_collectors.routes_collector import get_routes
from data_collectors.schedule_collector import get_schedules
from data_collectors.online_data_collector import get_online_data
from data_collectors.online_data_collector import remove_wrong_files


def get_all_data():
    # os.makedirs("static_data", exist_ok=True)
    # get_dict()
    # get_bus_stops()
    # get_routes()
    # get_schedules()
    # os.makedirs("online_data", exist_ok=True)
    # get_online_data()
    remove_wrong_files()
