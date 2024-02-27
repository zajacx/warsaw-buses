import requests
import json
import os


def get_routes():
    api_key = "d5a0df57-dbff-4d5b-b580-5949e1750cde"
    url = 'https://api.um.warszawa.pl/api/action/public_transport_routes/'

    request_params = {
        'apikey': api_key
    }

    response = requests.get(url, params=request_params).json()

    with open(os.path.join('./static_data', 'routes.json'), 'w') as file:
        json.dump(response["result"], file, indent=2)
