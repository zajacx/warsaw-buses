import json
import os
import geopandas as gpd
from shapely.geometry import Point
from shapely.prepared import prep
from datetime import datetime
from data_processing_scripts.dist_calculator import calculate_distance


# Dataframe prepared with geojson for districts data:
dist_df = gpd.read_file("static_data/districts.geojson")
# Polygon vertices:
dist_pg = [prep(v) for v in dist_df[1:]["geometry"]]


def read_json_file(file_path):
    with open(file_path, "r") as file:
        return json.load(file)


def write_json_file(data, file_path):
    with open(file_path, "w") as file:
        json.dump(data, file)


def filter_json(raw_json):
    filtered_json = {}
    for info in raw_json["result"]:
        filtered_json[info["VehicleNumber"]] = {
            "Line": info["Lines"],
            "Brigade": info["Brigade"],
            "Position": (info["Lon"], info["Lat"]),
            "Time": info["Time"]
        }

    return filtered_json


def calculate_district(point):
    for index, pg in enumerate(dist_pg):
        if pg.contains(point):
            return dist_df.loc[index + 1, "name"]

    return None


def process_file(data_dir, i, prev_data, segments_data, bus_positions):
    try:
        curr_file = read_json_file(os.path.join(data_dir, f"{i}.json"))
    except FileNotFoundError:
        return prev_data

    curr_data = filter_json(curr_file)

    for bus in prev_data:
        begin = prev_data.get(bus)
        end = curr_data.get(bus)

        if end is None:
            continue

        end["District"] = calculate_district(Point(end["Position"]))

        if end["District"] is None:
            continue

        try:
            time_1 = datetime.strptime(begin["Time"], "%Y-%m-%d %H:%M:%S")
            time_2 = datetime.strptime(end["Time"], "%Y-%m-%d %H:%M:%S")
            delta_t = time_2 - time_1
        except Exception:
            continue

        if 10 <= delta_t.seconds <= 60:
            distance = calculate_distance(begin["Position"], end["Position"])
            speed = (distance / delta_t.seconds) * 3.6

            segments_data.write(f"{begin['Position'][0]},{begin['Position'][1]},{end['Position'][0]},{end['Position'][1]},{end['District']},{speed}\n")
            bus_positions.append(end)

            if i == 1:
                bus_positions.append(begin)

    return curr_data


def prepare_speed_stats():
    cwd = os.getcwd()
    os.makedirs("filtered_data", exist_ok=True)

    segments_file_dir = os.path.join(cwd, "filtered_data", "filt_seg_busy.csv")
    segments_data = open(segments_file_dir, "w")
    segments_data.write("lon1,lat1,lon2,lat2,dist,speed\n")

    data_dir = os.path.join(cwd, "online_data", "busy_hours")
    files_count = 0
    for file in os.listdir(data_dir):
        file_path = os.path.join(data_dir, file)
        if os.path.isfile(file_path):
            files_count += 1

    prev_file = read_json_file(os.path.join(data_dir, "2.json"))
    prev_data = filter_json(prev_file)

    bus_positions = []

    for i in range(1, files_count):
        print(f"Processing file {i}")
        prev_data = process_file(data_dir, i, prev_data, segments_data, bus_positions)

    segments_data.close()
    write_json_file(bus_positions, os.path.join(cwd, "filtered_data", "bus_positions_busy.json"))
