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
