from datetime import datetime
import pprint
from functions.general import *


def format(response):
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

    list_of_countries = response['results']['places']
    list_of_airlines = response['results']['carriers']
    # Make 2 dictionaries: 1 for outbound trip, 1 for inbound trip
    formatted_response = {
        "pricingOptions": cheapest_flight_itinerary['pricingOptions'],
        "outbound": {
            "legId": cheapest_flight_itinerary["legIds"][0],
            "originAirport": {
                "name": f"{simple_comprehensify_dict('name', list_of_countries, outbound_leg['originPlaceId'])} Airport",
                "iata": simple_comprehensify_dict('iata', list_of_countries, outbound_leg['originPlaceId'])
            },
            "destinationAirport": {
                "name": f"{simple_comprehensify_dict('name', list_of_countries, outbound_leg['destinationPlaceId'])} Airport",
                "iata": simple_comprehensify_dict('iata', list_of_countries, outbound_leg['destinationPlaceId'])
            },
            'operatingCarrier': {
                'id': [i for i in outbound_leg['operatingCarrierIds']],
                'name': [value['name'] for key, value in list_of_airlines.items() for i in outbound_leg['operatingCarrierIds'] if key == i][0],
            },
            'marketingCarrier': {
                'id': [i for i in outbound_leg['operatingCarrierIds']],
                'name': [value['name'] for key, value in list_of_airlines.items() for i in outbound_leg['marketingCarrierIds'] if key == i][0],
            },
            'arrivalDateTime': {
                'date': convert_to_date(outbound_leg['arrivalDateTime']['day'], outbound_leg['arrivalDateTime']['month'], outbound_leg['arrivalDateTime']['year']),
                'time': convert_to_time(outbound_leg['arrivalDateTime']['hour'], outbound_leg['arrivalDateTime']['minute'], outbound_leg['arrivalDateTime']['second'])
            },
            'departureDateTime': {
                'date': convert_to_date(outbound_leg['departureDateTime']['day'], outbound_leg['departureDateTime']['month'], outbound_leg['departureDateTime']['year']),
                'time': convert_to_time(outbound_leg['departureDateTime']['hour'], outbound_leg['departureDateTime']['minute'], outbound_leg['departureDateTime']['second'])
            },
            'flightNos': [i['marketingFlightNumber'] for i in cheapest_segments['outbound'].values()]
        },
        "inbound": {
            "legId": cheapest_flight_itinerary["legIds"][1],
            "originAirport": {
                "name": f"{simple_comprehensify_dict('name', list_of_countries, inbound_leg['originPlaceId'])} Airport",
                "iata": simple_comprehensify_dict('iata', list_of_countries, inbound_leg['originPlaceId'])
            },
            "destinationAirport": {
                "name": f"{simple_comprehensify_dict('name', list_of_countries, inbound_leg['destinationPlaceId'])} Airport",
                "iata": simple_comprehensify_dict('iata', list_of_countries, inbound_leg['destinationPlaceId'])
            },
            'operatingCarrier': {
                'id': [i for i in inbound_leg['operatingCarrierIds']],
                'name': [value['name'] for key, value in list_of_airlines.items() for i in inbound_leg['operatingCarrierIds'] if key == i][0],
            },
            'marketingCarrier': {
                'id': [i for i in inbound_leg['operatingCarrierIds']],
                'name': [value['name'] for key, value in list_of_airlines.items() for i in inbound_leg['marketingCarrierIds'] if key == i][0],
            },
            'arrivalDateTime': {
                'date': convert_to_date(inbound_leg['arrivalDateTime']['day'], inbound_leg['arrivalDateTime']['month'], inbound_leg['arrivalDateTime']['year']),
                'time': convert_to_time(inbound_leg['arrivalDateTime']['hour'], inbound_leg['arrivalDateTime']['minute'], inbound_leg['arrivalDateTime']['second'])
            },
            'departureDateTime': {
                'date': convert_to_date(inbound_leg['departureDateTime']['day'], inbound_leg['departureDateTime']['month'], inbound_leg['departureDateTime']['year']),
                'time': convert_to_time(inbound_leg['departureDateTime']['hour'], inbound_leg['departureDateTime']['minute'], inbound_leg['departureDateTime']['second'])
            },
            'flightNos': [i['marketingFlightNumber'] for i in cheapest_segments['inbound'].values()]
        }
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
