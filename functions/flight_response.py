from datetime import datetime
import pprint
from functions.general import *
import sys

sys.path.append("..")

def format(response):
    cheap_list = response['sortingOptions']['cheapest']
    cheapest_flight_id = [i for i in cheap_list if i['score'] == 1][0]

    itinerary_list = response['results']['itineraries']
    cheapest_flight_itinerary = [value for key,value in itinerary_list.items() if key == cheapest_flight_id['itineraryId']][0]

    legs_list = response['results']['legs']
    cheapest_flight_details = [value for key,value in legs_list.items() if key == cheapest_flight_id['itineraryId']][0]

    list_of_countries = response['results']['places']
    list_of_airlines = response['results']['carriers']
    formatted_response = {
        'legIds': cheapest_flight_itinerary['legIds'],
        'pricingOptions': cheapest_flight_itinerary['pricingOptions'],
        'originAirport': {
            'originPlaceId': cheapest_flight_details['originPlaceId'],
            'originAirportName': simple_comprehensify_dict('name', list_of_countries, cheapest_flight_details['originPlaceId']),
            'originAirportIATA': simple_comprehensify_dict('iata', list_of_countries, cheapest_flight_details['originPlaceId'])
        },
        'destinationAirport': {
            'destinationPlaceId': cheapest_flight_details['destinationPlaceId'],
            'destinationAirportName': simple_comprehensify_dict('name', list_of_countries, cheapest_flight_details['destinationPlaceId']),
            'destinationAirportIATA': simple_comprehensify_dict('iata', list_of_countries, cheapest_flight_details['destinationPlaceId'])
        },
        'operatingCarrier': {
            'id': cheapest_flight_details['operatingCarrierIds'],
            'name': [value['name'] for key,value in list_of_airlines.items() for i in cheapest_flight_details['operatingCarrierIds'] if key == i][0],
        },
        'marketingCarrier': {
            'id': cheapest_flight_details['marketingCarrierIds'],
            'name': [value['name'] for key,value in list_of_airlines.items() for i in cheapest_flight_details['marketingCarrierIds'] if key == i][0],
        },
        'arrivalDateTime':{
            # 'date': datetime.strptime(f'{cheapest_flight_details["arrivalDateTime"]["day"]}/{cheapest_flight_details["arrivalDateTime"]["month"]}/{cheapest_flight_details["arrivalDateTime"]["year"]}', '%d/%m/%Y').date(),
            'date': convert_to_date(cheapest_flight_details['arrivalDateTime']['day'],cheapest_flight_details['arrivalDateTime']['month'],cheapest_flight_details['arrivalDateTime']['year']),
            'time': convert_to_time(cheapest_flight_details['arrivalDateTime']['hour'],cheapest_flight_details['arrivalDateTime']['minute'],cheapest_flight_details['arrivalDateTime']['second'])
        },
        'departureDateTime':{
            'date': convert_to_date(cheapest_flight_details['departureDateTime']['day'],cheapest_flight_details['departureDateTime']['month'],cheapest_flight_details['departureDateTime']['year']),
            'time': convert_to_time(cheapest_flight_details['departureDateTime']['hour'],cheapest_flight_details['departureDateTime']['minute'],cheapest_flight_details['departureDateTime']['second'])
        }
    }
    pprint.pprint(formatted_response)

    return formatted_response