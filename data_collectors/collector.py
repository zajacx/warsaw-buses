from data_collectors.dict_collector import get_dict
from data_collectors.bus_stops_collector import get_bus_stops
from data_collectors.routes_collector import get_routes
from data_collectors.schedule_collector import get_schedules

def get_all_data():
    get_dict()
    get_bus_stops()
    get_routes()
    # get_schedules()