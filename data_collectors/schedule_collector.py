import requests
import json
import os


def clean_dict(dict_to_clean):
    new_dict = dict()
    for i in dict_to_clean["values"]:
        new_dict[i["key"]] = i["value"]
    return new_dict


def get_schedules():
    # Data necessary to use API:
    api_key = "d5a0df57-dbff-4d5b-b580-5949e1750cde"
    api_id = "e923fa0e-d96c-43f9-ae6e-60518c9f3238"
    url = "https://api.um.warszawa.pl/api/action/dbtimetable_get"

    cwd = os.getcwd()

    # Create new directory for lines' schedules:
    schedule_dir = os.path.join(cwd, "./static_data/schedules")
    os.makedirs(schedule_dir, exist_ok=True)

    # Open routes data:
    routes_file_path = os.path.join(cwd, "./static_data/routes.json")
    routes = open(routes_file_path, 'r')

    data = json.load(routes)
    lines = list(data.keys())  # LIST OF ALL LINES

    # Get line info:
    for i in range(len(lines)):
        line_schedule = dict()
        line_info = []
        line_nr = lines[i]

        print(f"Downloading schedule for {line_nr}...")

        for route in data[line_nr]:
            stops_on_route = data[line_nr][route].keys()
            for stop_nr in stops_on_route:
                stop_data = data[line_nr][route][stop_nr]
                line_info.append(stop_data)

        for j in range(len(line_info)):
            request_params = {
                'id': api_id,
                'apikey': api_key,
                'busstopId': line_info[j]['nr_zespolu'],
                'busstopNr': line_info[j]['nr_przystanku'],
                'line': line_nr
            }
            bus_stop_key = request_params['busstopId'] + "/" + request_params['busstopNr']

            # API request:
            response = requests.get(url, params=request_params).json()
            for d in response["result"]:
                clean = clean_dict(d)
                brig_nr = clean["brygada"]
                if brig_nr not in line_schedule:
                    line_schedule[brig_nr] = dict()
                if bus_stop_key not in line_schedule[brig_nr]:
                    line_schedule[brig_nr][bus_stop_key] = []
                if clean["czas"] not in line_schedule[brig_nr][bus_stop_key]:
                    line_schedule[brig_nr][bus_stop_key].append(clean["czas"])

        # Create a new file with schedule for a line:
        new_file = f"{line_nr}.json"
        with open(os.path.join(schedule_dir, new_file), 'w') as s:
            json.dump(line_schedule, s, indent=2)

    # Close file
    routes.close()
