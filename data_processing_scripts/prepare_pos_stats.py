import os
import json
from datetime import datetime
from data_processing_scripts.dist_calculator import calculate_distance


def prepare_pos_stats():
    cwd = os.getcwd()

    # Get bus stops:
    bus_stops_file = os.path.join(cwd, "static_data/bus_stops.json")
    file = open(bus_stops_file, "r")
    bus_stops_list = json.load(file)
    file.close()

    # Get buses' positions:
    positions_file = os.path.join(cwd, "filtered_data", "bus_positions_busy.json")
    file = open(positions_file, "r")
    positions_list = json.load(file)
    file.close()

    filtered_bus_positions = []

    k = 0
    for bus in positions_list:
        print(k)
        k = k + 1
        # For each bus, find its expected stop at the current moment
        schedule = os.path.join(cwd, "static_data", "schedules", f"{bus['Line']}.json")
        try:
            file = open(schedule, "r")
        except Exception:
            continue

        schedule_list = json.load(file)
        file.close()

        if bus["Brigade"] not in schedule_list:
            continue  # data internal error

        # Get time:
        time = datetime.strptime(bus["Time"], "%Y-%m-%d %H:%M:%S").strftime("%H:%M:%S")
        # Iterate through all possible bus timestamps and find the best fit:
        min_time = 3600

        for stop in schedule_list[bus["Brigade"]]:
            if stop not in bus_stops_list:
                continue

            position = (float(bus_stops_list[stop]["dlug_geo"]), float(bus_stops_list[stop]["szer_geo"]))
            # Distance between bus and the stop:
            distance = calculate_distance(bus["Position"], position)

            if distance > 100:
                continue

            for t in schedule_list[bus["Brigade"]][stop]:
                # Wrong time parsing fix:
                if int(t[:2]) >= 24:
                    t = str(int(t[:2]) - 24) + t[2:]

                # Current time difference:
                delta_t = abs((datetime.strptime(t, "%H:%M:%S") - datetime.strptime(time, "%H:%M:%S")).seconds)

                # Linear search for the smallest time difference:
                min_time = min(min_time, delta_t)

            if min_time >= 3600:
                continue

            # Delay:
            bus["Time"] = min_time
            filtered_bus_positions.append(bus)

    # Save to file:
    filtered_positions_file = open(os.path.join(cwd, "filtered_data", "filt_bus_positions_busy.json"), "w")
    json.dump(filtered_bus_positions, filtered_positions_file, indent=2)
