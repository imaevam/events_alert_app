import datetime
import json
import os
import pprint
import requests
from webapp.models import db
from webapp.event.models import Event
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


def get_payload(url):
    url = f"https://afisha.ru/{url}"
    return requests.get(url=url, headers={'Accept': 'application/json'}).json()


def convert_date(date): 
    date_format = '%Y-%m-%dT%H:%M:%S'
    date_update = datetime.datetime.strptime(date, date_format)
    return date_update


def get_description(url, category):
    url = url[1:]
    main_func = get_payload(url)
    if category == 'movie':
        data_descr = main_func['MovieCard']['Info']['Description']
    elif category == 'exhibition':
        if main_func['ExhibitionInfo']['DistributorInfo'] is None:
            data_descr = main_func['ExhibitionInfo']['Description']
        elif main_func['ExhibitionInfo']['Description'] == '':
            data_descr = main_func['ExhibitionInfo']['DistributorInfo']['Text']
        else: 
            data_descr = None
    elif category == 'theatre':
        data_descr = main_func['PerformanceInfo']['Description']
    elif category == 'concert':
        data_descr = main_func['ConcertInfo']['Description']
    return data_descr
    

def collect_details(category_lst, category):
    tiles = [tile for item in category_lst for tile in item['Tiles']]
    events = []
    for tile in tiles:
        name = tile['Name']
        genre = tile['Badge']
        date_min, date_max = tile['ScheduleInfo']['MaxScheduleDate'], tile['ScheduleInfo']['MinScheduleDate'] 
        if isinstance(date_min, str) and isinstance(date_max, str):
            date_start, date_finish = convert_date(date_min), convert_date(date_max)
        else: 
            date_start, date_finish = None, None
        address = tile['Notice']['PlaceUrl']['Address'] 
        place = tile['Notice']['PlaceUrl']['Name'] 
        price = tile['ScheduleInfo']['MinPrice']
        url = tile['Url']
        description = get_description(url, category)
        event = Event(name=name, genre=genre, date_start=date_start, date_finish=date_finish, address=address, place=place, price=price, url=url, description=description)
        events.append(event)
        db.session.bulk_save_objects(events)
        # без коммита, потому что в models.py session_options={'autocommit': True}

#img_url = tile['Image630x315']['Url']


