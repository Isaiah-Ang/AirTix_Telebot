import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()


def get_airports_json():
    airport_json_url = 'https://travelpayouts-travelpayouts-flight-data-v1.p.rapidapi.com/data/en-GB/airports.json'
    header = {
        'X-Access-Token': os.getenv('X_ACCESS_API'),
        'X-RapidAPI-Key': os.getenv('X_RAPIDAPI_KEY'),
        'X-RapidAPI-Host': 'travelpayouts-travelpayouts-flight-data-v1.p.rapidapi.com'
    }
    airport_json_response = requests.get(
        url=airport_json_url, headers=header
    )
    y = airport_json_response.json()
    json_object = json.dumps(y, indent=4)

    with open("cities.json", "w") as outfile:
        outfile.write(json_object)


def get_cities_json():
    city_json_url = 'https://travelpayouts-travelpayouts-flight-data-v1.p.rapidapi.com/data/en-GB/cities.json'
    header = {
        'X-Access-Token': os.getenv('X_ACCESS_API'),
        'X-RapidAPI-Key': os.getenv('X_RAPIDAPI_KEY'),
        'X-RapidAPI-Host': 'travelpayouts-travelpayouts-flight-data-v1.p.rapidapi.com'
    }
    city_json_response = requests.get(
        url=city_json_url, headers=header
    )
    y = city_json_response.json()
    json_object = json.dumps(y, indent=4)

    with open("cities.json", "w") as outfile:
        outfile.write(json_object)


get_cities_json()
