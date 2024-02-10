import requests
import json
import os


def clean_dict(dict_to_clean):
    new_dict = dict()
    for i in dict_to_clean["values"]:
        new_dict[i["key"]] = i["value"]
    return new_dict


def get_bus_stops():
    # Data necessary to use API:
    api_key = "d5a0df57-dbff-4d5b-b580-5949e1750cde"
    api_id = "1c08a38c-ae09-46d2-8926-4f9d25cb0630"
    url = "https://api.um.warszawa.pl/api/action/dbstore_get"

    # API request parameters:
    request_params = {
        'id': api_id,
        'apikey': api_key
    }

    response = requests.get(url, params=request_params).json()
    clean_data = dict()

    # Clean the data and create a json:
    for data in response['result']:
        clean = clean_dict(data)
        key = '/'.join((clean['zespol'], clean['slupek']))
        clean_data[key] = clean

    # Create new file and save data:
    with open(os.path.join('./static_data', 'bus_stops.json'), 'w') as file:
        json.dump(clean_data, file, indent=2)
