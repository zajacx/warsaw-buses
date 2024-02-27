import os
import json
from datetime import datetime
from data_processing_scripts.dist_calculator import calculate_distance


def read_json_file(file_path):
    with open(file_path, "r") as file:
        return json.load(file)


def write_json_file(data, file_path):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=2)


def get_bus_stops(cwd):
    bus_stops_file = os.path.join(cwd, "static_data/bus_stops.json")
    return read_json_file(bus_stops_file)


def get_positions_list(cwd):
    positions_file = os.path.join(cwd, "filtered_data", "bus_positions_busy.json")
    return read_json_file(positions_file)


def get_schedule_list(cwd, bus_line):
    schedule_file = os.path.join(cwd, "static_data", "schedules", f"{bus_line}.json")
    return read_json_file(schedule_file)


def filter_bus_positions(bus_stops_list, positions_list, cwd):
    filtered_bus_positions = []

    for k, bus in enumerate(positions_list):
        print(f"Progress: {k}/{len(positions_list)}")

        schedule_list = get_schedule_list(cwd, bus['Line'])

        if bus["Brigade"] not in schedule_list:
            continue  # data internal error

        time = datetime.strptime(bus["Time"], "%Y-%m-%d %H:%M:%S").strftime("%H:%M:%S")
        min_time = 3600

        for stop in schedule_list[bus["Brigade"]]:
            if stop not in bus_stops_list:
                continue

            position = (float(bus_stops_list[stop]["dlug_geo"]), float(bus_stops_list[stop]["szer_geo"]))
            distance = calculate_distance(bus["Position"], position)

            if distance > 100:
                continue

            for t in schedule_list[bus["Brigade"]][stop]:
                t = fix_wrong_time_format(t)

                delta_t = abs((datetime.strptime(t, "%H:%M:%S") - datetime.strptime(time, "%H:%M:%S")).seconds)
                min_time = min(min_time, delta_t)

            if min_time >= 3600:
                continue

            bus["Time"] = min_time
            filtered_bus_positions.append(bus)

    return filtered_bus_positions


def fix_wrong_time_format(time_str):
    if int(time_str[:2]) >= 24:
        return str(int(time_str[:2]) - 24) + time_str[2:]
    return time_str


def prepare_pos_stats():
    cwd = os.getcwd()
    bus_stops_list = get_bus_stops(cwd)
    positions_list = get_positions_list(cwd)
    filtered_bus_positions = filter_bus_positions(bus_stops_list, positions_list, cwd)
    write_json_file(filtered_bus_positions, os.path.join(cwd, "filtered_data", "filt_bus_positions_busy.json"))
