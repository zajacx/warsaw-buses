import requests
import json
import os


def clean_dict(info):
    new_dict = dict()
    for dic in info["values"]:
        new_dict[dic["key"]] = dic["value"]
    return new_dict

# Data necessary to use API:
api_key = "d5a0df57-dbff-4d5b-b580-5949e1750cde"
api_id = "e923fa0e-d96c-43f9-ae6e-60518c9f3238"
url = "https://api.um.warszawa.pl/api/action/dbtimetable_get"

# auxiliary? idk
busstopId = '7009'
busstopNr = '01'
line = '523'

# API request parameters:
request_params = {
    'id': api_id,
    'busstopId': busstopId,
    'busstopNr': busstopNr,
    'line': line,
    'apikey': api_key
}

response = requests.get(url, params=request_params).json()


# Create new file and save static_data:
with open(os.path.join('../static_data', 'bus_lines.json'), 'w') as file:
    json.dump(response["result"], file, indent=2)
