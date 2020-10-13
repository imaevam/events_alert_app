import datetime
import json
import os

import requests
import pprint

cur_dir = 'C:\\projects\\final\\images'

def get_payload(url):
    url = f"https://afisha.ru/{url}"
    return requests.get(url=url, headers={'Accept': 'application/json'}).json()


def save_img(img_url, path_to_save, category_lst):
    if not os.path.exists(path_to_save):
        os.mkdir(path_to_save)
    response = requests.get(img_url)
    image_name = img_url.split('/')[-1]
    save_path = os.path.join(path_to_save, image_name) # (os.getcwd(), filename)
    if response.status_code == 200:
        with open(save_path, 'wb') as handler:
            handler.write(response.context)
    return save_path # импортировать в model


def convert_date(date): 
    date_format = '%Y-%m-%dT%H:%M:%S'
    date_update = datetime.datetime.strptime(date, date_format)
    return date_update


def get_description(url, category):
    url = url[1:]
    if category == 'movie':
        data_descr = get_payload(url)['MovieCard']['Info']['Description']
    elif category == 'exhibition': # TypeError: 'NoneType' object is not subscriptable
        if get_payload(url)['ExhibitionInfo']['DistributorInfo'] == None:
            data_descr = get_payload(url)['ExhibitionInfo']['Description']     # иногда бывает 'description': '', 'DistributorInfo': None
        elif get_payload(url)['ExhibitionInfo']['Description'] == '':
            data_descr = get_payload(url)['ExhibitionInfo']['DistributorInfo']['Text']
        else: 
            data_descr = None
    elif category == 'theatre':
        data_descr = get_payload(url)['PerformanceInfo']['Description']
    elif category == 'concert':
        data_descr = get_payload(url)['ConcertInfo']['Description']
    return data_descr
    

def collect_details(category_lst, category):
    all_data = [] 
    tiles = [tile for item in category_lst for tile in item['Tiles']]
    for tile in tiles:
        name = tile['Name']
        genre = tile['Badge']
        date_start, date_finish = tile['ScheduleInfo']['MaxScheduleDate'], tile['ScheduleInfo']['MinScheduleDate'] 
        if isinstance(date_start, str) and isinstance(date_finish, str):
            date_min, date_max = convert_date(date_start), convert_date(date_finish)
        else: 
            date_min, date_max = None, None
        address = tile['Notice']['PlaceUrl']['Address']
        place = tile['Notice']['PlaceUrl']['Name']
        price = tile['ScheduleInfo']['MinPrice']
        url = tile['Url']
        description = get_description(url, category)
        img_url = tile['Image630x315']['Url']
        all_data.append({
            'category': category,
            'name': name,
            'genre': genre,
            'date_start': date_min,
            'date_finish': date_max,
            'address': address,
            'place': place,
            'price': price,
            'url': url,
            'description': description,
            'img_path': img_url
        })
    return all_data