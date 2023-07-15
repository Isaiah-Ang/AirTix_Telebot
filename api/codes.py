import json
import country_converter as coco

cc = coco.CountryConverter()

cities = open('cities.json')
city_data = json.load(cities)

airports = open('airports.json')
airport_data = json.load(airports)


def convert_country_code(city, country):
    country_code = cc.convert(names=country, to='ISO2')
    return convert_city(city, country_code)


def convert_city(city, country):
    city_index = list(filter(lambda x: city_data[x]['name_translations']['en'] ==
                      city and city_data[x]['country_code'] == country, range(len(city_data))))
    city_code = city_data[city_index[0]]['code']

    # Check if the city exists

    return convert_airport_code(city_code)


def convert_airport_code(city):
    airport_code = [{"name": x['name_translations']['en'], "code": x['code']}
                    for x in airport_data if x['city_code'] == city]
    return airport_code
