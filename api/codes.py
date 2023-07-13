import json
import requests
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
    city_code = str()
    for x in city_data:
        if x['name_translations']['en'] == city and x['country_code'] == country:
            # print(x['name_translations']['en'])
            # city_code.append(x['name_translations']["en"])
            city_code = x['code']

    print(city_code)
    return convert_airport_code(city_code)
    # print(len(city_data))


def convert_airport_code(city):
    airport_code = list()
    for x in airport_data:
        if x['city_code'] == city:
            airport_code.append(
                {"name": x['name_translations']['en'], "code": x['code']})

    print(airport_code)
    return airport_code


# convert_country_code('Melbourne', 'Australia')
# convert_airport_code()
# convert_city()