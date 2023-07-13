import requests
import os
from dotenv import load_dotenv, dotenv_values
import pprint

load_dotenv()

def access_token_post_request(): 
    url = 'https://test.api.amadeus.com/v1/security/oauth2/token'
    header = {'Content-Type': 'application/x-www-form-urlencoded',}
    data_code = f'grant_type=client_credentials&client_id={os.getenv("amadeus_client_id")}&client_secret={os.getenv("amadeus_secret_key")}'

    access_token = requests.post(url=url, headers=header, data=data_code)

    x = access_token.json()
    response_access_token = x['access_token']
    return response_access_token

def get_flight_offers(response_access_token):
    flight_offers_url = 'https://test.api.amadeus.com/v2/shopping/flight-offers'
    header = {'Authorization': f"Bearer {response_access_token}",}
    data_code={
        'originLocationCode':'SYD',
        'destinationLocationCode':'BKK',
        'departureDate':'2023-08-10',
        'adults':1,
        'max': 1
    }
    flight_offer_response = requests.get(url=flight_offers_url, headers=header, params=data_code)
    y= flight_offer_response.json()
    pprint.pprint(y)

##Function currently not supported
def flight_cheapest_date(response_access_token):
    flight_cheapest_date_url = 'https://test.api.amadeus.com/v1/shopping/flight-dates'
    header = {'Authorization': f"Bearer {response_access_token}",}
    data_code={
        'origin':'SYD',
        'destination':'BKK',
    }
    flight_cheapest_date_response = requests.get(url=flight_cheapest_date_url, headers=header, params=data_code)
    z = flight_cheapest_date_response.json()
    pprint.pprint(z)
    

token_key = access_token_post_request()
get_flight_offers(token_key)