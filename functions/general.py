from datetime import datetime


def simple_comprehensify_dict(value_name, condition1: any, condition2: any):
    row = [value[value_name] if value_name != None else value for key,
           value in condition1.items() if key == condition2][0]
    return row


def convert_to_date(date: str, month: str, year: str):
    date = datetime.strptime(f"{date}/{month}/{year}", "%d/%m/%Y").date()
    return date


def convert_to_time(hour: str, minute: str, second: str):
    time = datetime.strptime(f"{hour}:{minute}:{second}", '%H:%M:%S')
    return time


def iterate(iterable):
    iterator = iter(iterable)
    item = next(iterator)

    for next_item in iterator:
        yield item, next_item
        item = next_item

    yield item, None


def format_message(data):
    message = ''
    for item, next_item in iterate(data.items()):
        i = item[1]

        if next_item != None:
            delta = next_item[1]['departureDateTime']['time'] - \
                i['arrivalDateTime']['time']
            sec = delta.total_seconds()
            min = (sec / 60) / 10
            hours = sec / (60 * 60)

            print(i['arrivalDateTime']['time'].strftime('%H:%M'))

        tab = '\t'
        next_line = '\n'

        message += f"{i['flightNo']}\n{i['departureDateTime']['time'].strftime('%H:%M')}\t{i['originAirport']['iata']} {i['originAirport']['name']}\n{i['arrivalDateTime']['time'].strftime('%H:%M')}\t{i['destinationAirport']['iata']} {i['destinationAirport']['name']}\n\n{str(abs(int(hours))) + 'h' + str(abs(int(min))) + tab + 'Layover' + next_line * 2 if next_item != None else ''}"

    return message
