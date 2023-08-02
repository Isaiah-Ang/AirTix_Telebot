from datetime import datetime
from functions.general import *


def format_direct_flight(response):
    # Function to retrieve the cheapest direct one-way flight
    flight_stops = response['stats']['itineraries']['stops']
    direct_flight_cheapest_price = flight_stops['direct']['total']['minPrice']['amount']

    all_direct_legs = {key: value for key,
                       value in response['results']['legs'].items() if len(value['segmentIds']) == 1}

    all_direct_itineraries = {key: value for key, value in response['results']
                              ['itineraries'].items() for i in all_direct_legs.keys() if value['legIds'][0] == i}

    cheapest_itinerary = [i for i in all_direct_itineraries.values() if i['pricingOptions']
                          [0]['price']['amount'] == direct_flight_cheapest_price][0]

    cheapest_legs = [value for key, value in all_direct_legs.items(
    ) if key == cheapest_itinerary['legIds'][0]][0]

    cheapest_segments = [value for key, value in response['results']['segments'].items(
    ) if key == cheapest_legs['segmentIds'][0]][0]

    list_of_countries = response['results']['places']
    list_of_airlines = response['results']['carriers']

    list_of_countries = response['results']['places']
    list_of_airlines = response['results']['carriers']
    formatted_response = {
        'legIds': cheapest_itinerary['legIds'],
        'pricingOptions': cheapest_itinerary['pricingOptions'],
        'originAirport': {
            'originPlaceId': cheapest_legs['originPlaceId'],
            'originAirportName': f"{simple_comprehensify_dict('name', list_of_countries, cheapest_legs['originPlaceId'])} Airport",
            'originAirportIATA': simple_comprehensify_dict('iata', list_of_countries, cheapest_legs['originPlaceId'])
        },
        'destinationAirport': {
            'destinationPlaceId': cheapest_legs['destinationPlaceId'],
            'destinationAirportName': f"{simple_comprehensify_dict('name', list_of_countries, cheapest_legs['destinationPlaceId'])} Airport",
            'destinationAirportIATA': simple_comprehensify_dict('iata', list_of_countries, cheapest_legs['destinationPlaceId'])
        },
        'operatingCarrier': {
            'id': cheapest_legs['operatingCarrierIds'],
            'name': [value['name'] for key, value in list_of_airlines.items() for i in cheapest_legs['operatingCarrierIds'] if key == i][0],
        },
        'marketingCarrier': {
            'id': cheapest_legs['marketingCarrierIds'],
            'name': [value['name'] for key, value in list_of_airlines.items() for i in cheapest_legs['marketingCarrierIds'] if key == i][0],
        },
        'arrivalDateTime': {
            'date': convert_to_date(cheapest_legs['arrivalDateTime']['day'], cheapest_legs['arrivalDateTime']['month'], cheapest_legs['arrivalDateTime']['year']),
            'time': convert_to_time(cheapest_legs['arrivalDateTime']['hour'], cheapest_legs['arrivalDateTime']['minute'], cheapest_legs['arrivalDateTime']['second'])
        },
        'departureDateTime': {
            'date': convert_to_date(cheapest_legs['departureDateTime']['day'], cheapest_legs['departureDateTime']['month'], cheapest_legs['departureDateTime']['year']),
            'time': convert_to_time(cheapest_legs['departureDateTime']['hour'], cheapest_legs['departureDateTime']['minute'], cheapest_legs['departureDateTime']['second'])
        },
        'flightNo': f'{[value["displayCode"] for key, value in list_of_airlines.items() for i in cheapest_legs["marketingCarrierIds"] if key == i][0]} {cheapest_segments["marketingFlightNumber"]}'
    }

    return formatted_response
