from datetime import datetime
import pprint
from functions.general import *


def format(response):
    list_of_countries = response['results']['places']
    list_of_airlines = response['results']['carriers']

    cheap_list = response['sortingOptions']['cheapest']
    cheapest_flight_id = [i for i in cheap_list if i['score'] == 1][0]

    itinerary_list = response['results']['itineraries']
    cheapest_flight_itinerary = [value for key, value in itinerary_list.items(
    ) if key == cheapest_flight_id['itineraryId']][0]

    legs_list = response['results']['legs']
    cheapest_legs = [{key: value} for i in cheapest_flight_itinerary['legIds']
                     for key, value in legs_list.items() if key == i]

    outbound_leg = list(cheapest_legs[0].values())[0]
    inbound_leg = list(cheapest_legs[1].values())[0]

    cheapest_segments = {
        "outbound": {key: value for j in outbound_leg['segmentIds']
                     for key, value in response['results']['segments'].items() if key == j},
        "inbound": {key: value for j in inbound_leg['segmentIds']
                    for key, value in response['results']['segments'].items() if key == j}
    }

    segments = {
        "outbound": {},
        "inbound": {},
    }

    for key, value in cheapest_segments["outbound"].items():
        segment = {
            key: {
                "flightNo": f"{[airline_value['displayCode'] for airline_key, airline_value in list_of_airlines.items() if airline_key == value['marketingCarrierId']][0]}{value['marketingFlightNumber']}",
                "originAirport": {
                    "name": f"{simple_comprehensify_dict('name', list_of_countries, value['originPlaceId'])} Airport",
                    "iata": f"{simple_comprehensify_dict('iata', list_of_countries, value['originPlaceId'])}"
                },
                "destinationAirport": {
                    "name": f"{simple_comprehensify_dict('name', list_of_countries, value['destinationPlaceId'])} Airport",
                    "iata": f"{simple_comprehensify_dict('iata', list_of_countries, value['destinationPlaceId'])}"
                },
                "operatingCarrier": {
                    'id': [value['operatingCarrierId']],
                    'name': [airline_value['name'] for airline_key, airline_value in list_of_airlines.items() if airline_key == value['operatingCarrierId']],
                },
                'marketingCarrier': {
                    'id': [value['marketingCarrierId']],
                    'name': [marketing_value['name'] for marketing_key, marketing_value in list_of_airlines.items() if marketing_key == value['marketingCarrierId']],
                },
                'arrivalDateTime': {
                    'date': convert_to_date(value['arrivalDateTime']['day'], value['arrivalDateTime']['month'], value['arrivalDateTime']['year']),
                    'time': convert_to_time(value['arrivalDateTime']['hour'], value['arrivalDateTime']['minute'], value['arrivalDateTime']['second'])
                },
                'departureDateTime': {
                    'date': convert_to_date(value['departureDateTime']['day'], value['departureDateTime']['month'], value['departureDateTime']['year']),
                    'time': convert_to_time(value['departureDateTime']['hour'], value['departureDateTime']['minute'], value['departureDateTime']['second'])
                },
            }
        }
        segments['outbound'].update(segment)

    for key, value in cheapest_segments["inbound"].items():
        segment = {
            key: {
                "flightNo": f"{[airline_value['displayCode'] for airline_key, airline_value in list_of_airlines.items() if airline_key == value['marketingCarrierId']][0]}{value['marketingFlightNumber']}",
                "originAirport": {
                    "name": f"{simple_comprehensify_dict('name', list_of_countries, value['originPlaceId'])} Airport",
                    "iata": f"{simple_comprehensify_dict('iata', list_of_countries, value['originPlaceId'])}"
                },
                "destinationAirport": {
                    "name": f"{simple_comprehensify_dict('name', list_of_countries, value['destinationPlaceId'])} Airport",
                    "iata": f"{simple_comprehensify_dict('iata', list_of_countries, value['destinationPlaceId'])}"
                },
                "operatingCarrier": {
                    'id': [value['operatingCarrierId']],
                    'name': [airline_value['name'] for airline_key, airline_value in list_of_airlines.items() if airline_key == value['operatingCarrierId']],
                },
                'marketingCarrier': {
                    'id': [value['marketingCarrierId']],
                    'name': [marketing_value['name'] for marketing_key, marketing_value in list_of_airlines.items() if marketing_key == value['marketingCarrierId']],
                },
                'arrivalDateTime': {
                    'date': convert_to_date(value['arrivalDateTime']['day'], value['arrivalDateTime']['month'], value['arrivalDateTime']['year']),
                    'time': convert_to_time(value['arrivalDateTime']['hour'], value['arrivalDateTime']['minute'], value['arrivalDateTime']['second'])
                },
                'departureDateTime': {
                    'date': convert_to_date(value['departureDateTime']['day'], value['departureDateTime']['month'], value['departureDateTime']['year']),
                    'time': convert_to_time(value['departureDateTime']['hour'], value['departureDateTime']['minute'], value['departureDateTime']['second'])
                },
            }
        }
        segments['inbound'].update(segment)

    # Make 2 dictionaries: 1 for outbound trip, 1 for inbound trip
    formatted_response = {
        "pricingOptions": cheapest_flight_itinerary['pricingOptions'],
        "outbound": segments['outbound'],
        "inbound": segments['inbound']
    }
    return (formatted_response)


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
