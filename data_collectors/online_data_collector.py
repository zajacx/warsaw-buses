import requests
import json
import time
import os


def get_online_data():
    # Data necessary to use API:
    api_key = "d5a0df57-dbff-4d5b-b580-5949e1750cde"
    url = 'https://api.um.warszawa.pl/api/action/busestrams_get/'
    request_params = {
        'resource_id': 'f2e5503e-927d-4ad3-9500-4ab9e55deb59',
        'type':	'1',
        'apikey': api_key
    }

    cwd = os.getcwd()

    # Create new directory for online data:
    online_dir = os.path.join(cwd, "./online_data")
    os.makedirs(online_dir, exist_ok=True)

    data_dir = os.path.join(online_dir, "late_hours")
    os.makedirs(data_dir, exist_ok=True)

    # Send request each 10 seconds to get at least one during one minute:
    for i in range(300):
        print(f"Progress: {i}/300")
        if i != 0:
            time.sleep(10)

        response = requests.get(url, params=request_params).json()

        # Create a file for i-th moment:
        act_loc = os.path.join(data_dir, f"{i}.json")
        with open(act_loc, 'w') as file:
            json.dump(response, file, indent=2)


def remove_wrong_files():
    cwd = os.getcwd()
    directory = os.path.join(cwd, "online_data", "busy_hours")
    for i in range(600):
        file_dir = os.path.join(directory, f"{i}.json")
        file = open(file_dir, "r")
        data = json.load(file)
        file.close()
        if data["result"] == "B\u0142\u0119dna metoda lub parametry wywo\u0142ania":
            try:
                os.remove(file_dir)
                # print(f"File {file_dir} removed successfully.")
            except FileNotFoundError:
                print(f"File {file_dir} not found.")
            except Exception as e:
                print(f"An error occurred: {e}")
        else:
            continue
