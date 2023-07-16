import requests
import os
from dotenv import load_dotenv, dotenv_values
import pprint

load_dotenv()


def access_token_post_request():
    url = 'https://test.api.amadeus.com/v1/security/oauth2/token'
    header = {'Content-Type': 'application/x-www-form-urlencoded', }
    data_code = f'grant_type=client_credentials&client_id={os.getenv("CLIENT_ID")}&client_secret={os.getenv("CLIENT_SECRET")}'

    access_token = requests.post(url=url, headers=header, data=data_code)

    x = access_token.json()
    response_access_token = x['access_token']
    return response_access_token


def get_flight_offers(origin: str, destination: str, response_access_token: str):
    flight_offers_url = 'https://test.api.amadeus.com/v2/shopping/flight-offers'
    header = {'Authorization': f"Bearer {response_access_token}", }
    data_code = {
        'originLocationCode': 'SYD',
        'destinationLocationCode': 'BKK',
        'departureDate': '2023-08-10',
        'adults': 1,
        'max': 1
    }
    flight_offer_response = requests.get(
        url=flight_offers_url, headers=header, params=data_code)
    y = flight_offer_response.json()
    pprint.pprint(y)

# Function currently not supported


def flight_cheapest_date(origin: str, destination: str, response_access_token: str):
    flight_cheapest_date_url = 'https://test.api.amadeus.com/v1/shopping/flight-dates'
    header = {'Authorization': f"Bearer {response_access_token}", }
    data_code = {
        # Plug origin & destination variables here
        'origin': 'SYD',
        'destination': 'BKK',
    }
    flight_cheapest_date_response = requests.get(
        url=flight_cheapest_date_url, headers=header, params=data_code)
    z = flight_cheapest_date_response.json()
    pprint.pprint(z)

# travel payouts api


def cheapest_tickets(origin_country_code: str, destination_country_code: str, depart_date: str, arrival_date: str):
    cheapest_tickets_url = "https://travelpayouts-travelpayouts-flight-data-v1.p.rapidapi.com/v1/prices/cheap"
    data_code = {"origin": "SIN", "page": "None",
                 "currency": "USD", "destination": "ICN"}
    headers = {
        "X-Access-Token": f'{os.getenv("travel_payout_token")}',
        "X-RapidAPI-Key": f'{os.getenv("rapid_api_key")}',
        "X-RapidAPI-Host": "travelpayouts-travelpayouts-flight-data-v1.p.rapidapi.com"
    }
    response = requests.get(cheapest_tickets_url,
                            headers=headers, params=data_code)
    return response


def non_stop_tickets():
    url = "https://travelpayouts-travelpayouts-flight-data-v1.p.rapidapi.com/v1/prices/direct/"

    querystring = {"destination": "ICN", "origin": "SIN",
                   "return_date": "2023-09-19", "depart_date": "2023-09-02", "currency": "RUB"}

    headers = {
        "X-Access-Token": f'{os.getenv("TRAVELPAYOUTSAPI_KEY")}',
        "X-RapidAPI-Key": f'{os.getenv("RAPIDAPI_KEY")}',
        "X-RapidAPI-Host": "travelpayouts-travelpayouts-flight-data-v1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    return response


trav_pay_cheapest_tickets = non_stop_tickets()
print(trav_pay_cheapest_tickets.json())
