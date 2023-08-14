import requests
import os
from dotenv import load_dotenv, dotenv_values
import json

load_dotenv()


def skyscan_tickets(origin_airport: str, destination_airport: str):
    url = 'https://partners.api.skyscanner.net/apiservices/v3/flights/live/search/create'

    querystring = json.dumps({
        "query": {
            "market": "UK",
            "locale": "en-GB",
            "currency": "SGD",
            "queryLegs": [{
                "origin_place_id": {
                    "iata": f'{origin_airport}'
                },
                "destination_place_id": {
                    "iata": f'{destination_airport}'
                },
                "date": {
                    "year": 2023,
                    "month": 12,
                    "day": 22
                }
            },
                {
                "origin_place_id": {
                    "iata": f'{destination_airport}'
                },
                "destination_place_id": {
                    "iata": f'{origin_airport}'
                },
                "date": {
                    "year": 2023,
                    "month": 12,
                    "day": 26
                }
            }],
            "cabinClass": "CABIN_CLASS_ECONOMY",
            "adults": 1
        }
    })

    headers = {
        "x-api-key": f'{os.getenv("SKYSCANNERAPI_KEY")}'
    }

    response = requests.post(url, headers=headers, data=querystring)

    data = response.json()['content']

    return data
