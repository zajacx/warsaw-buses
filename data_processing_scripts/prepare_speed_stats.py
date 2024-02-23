import json
import os
import geopandas as gpd
from shapely.geometry import Point
from shapely.prepared import prep
from datetime import datetime
from data_processing_scripts.dist_calculator import calculate_distance


def filter_json(raw_json):
    filtered_json = dict()
    for info in raw_json["result"]:
        filtered_json[info["VehicleNumber"]] = {
            "Line": info["Lines"],
            "Brigade": info["Brigade"],
            "Position": (info["Lon"], info["Lat"]),
            "Time": info["Time"]
        }

    return filtered_json


def prepare_speed_stats():
    # Dataframe prepared with geojson for districts data:
    dist_df = gpd.read_file("static_data/districts.geojson")
    # Polygon vertices:
    dist_pg = [prep(v) for v in dist_df[1:]["geometry"]]

    cwd = os.getcwd()
    # New directory for filtered data:
    os.makedirs("filtered_data", exist_ok=True)

    # File for all segments that buses pass:
    segments_data = open(os.path.join(cwd, "filtered_data", "filt_seg_busy.csv"), "w")
    segments_data.write("lon1,lat1,dist1,lon2,lat2,dist2,speed\n")

    # Files directory:
    data_dir = os.path.join(cwd, "online_data", "busy_hours")
    # Count the number of files:
    files_count = sum(1 for file in os.listdir(data_dir) if os.path.isfile(os.path.join(data_dir, file)))

    # Prepare initial file:
    prev_file = open(os.path.join(data_dir, "2.json"))
    prev_list = json.load(prev_file)
    prev_data = filter_json(prev_list)

    # Collect positions of buses while calculating speed:
    bus_positions = []

    # Get data from all files:
    for i in range(1, files_count):
        try:
            curr_file = open(os.path.join(data_dir, f"{i}.json"), "r")
        except FileNotFoundError:
            continue

        curr_list = json.load(curr_file)
        curr_data = filter_json(curr_list)

        for bus in prev_data:
            # Current segment:
            begin = prev_data.get(bus)
            end = curr_data.get(bus)

            if end is None:
                continue

            dist_1 = 0
            dist_2 = 0

            # Get info about previous and current district:
            for index, pg in enumerate(dist_pg):
                if pg.contains(Point(end["Position"])):
                    dist_2 = dist_df.loc[index + 1, "name"]
                else:
                    dist_2 = None

                if pg.contains(Point(begin["Position"])):
                    dist_1 = dist_df.loc[index + 1, "name"]
                else:
                    dist_1 = None

            if dist_1 is None or dist_2 is None:
                continue

            # Calculate time difference (skip in case of an error):
            try:
                time_1 = datetime.strptime(begin["Time"], "%Y-%m-%d %H:%M:%S")
                time_2 = datetime.strptime(end["Time"], "%Y-%m-%d %H:%M:%S")
                delta_t = time_2 - time_1
            except Exception:
                continue

            # We expect time difference to be between 10 and 60:
            if not (10 <= delta_t.seconds <= 60):
                continue

            # Calculate distance and speed:
            distance = calculate_distance(begin["Position"], end["Position"])
            speed = distance / delta_t.seconds
            speed = speed * 3.6

            # Write statistics to csv:
            segments_data.write(f"{begin['Position'][0]},{begin['Position'][1]},{dist_1},{end['Position'][0]},{end['Position'][1]},{dist_2},{speed}\n")
            print(f"Prepared {i}. data")

            # Save bus' position:
            bus_positions.append(end)
            if i == 1:
                bus_positions.append(begin)

        prev_file.close()
        prev_file = curr_file
        prev_data = curr_data

    prev_file.close()
    segments_data.close()
    positions_file = open(os.path.join(cwd, "filtered_data", "bus_positions_busy.json"), "w")
    json.dump(bus_positions, positions_file)
