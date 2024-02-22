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
