import json
import os

import requests
import pprint

#cur_dir = 'C:\\projects\\final\\images'

def get_payload(url):
    url = f"https://afisha.ru/{url}"
    return requests.get(url=url, headers={'Accept': 'application/json'}).json()


def save_img(url, path_to_save):
    if not os.path.exists(path_to_save):
        os.mkdir(path_to_save)
    pass

def convert_date(date):
    date = str(date)
    out = date.replace("T"," ")
    return out
     
def collect_exhibitions(exhibition_lst):
    exhb_data = [] 
    tiles = [tile for item in exhibition_lst for tile in item['Tiles']]
    for tile in tiles:
        name = tile['Name']
        genre = tile['Badge']
        date_start, date_finish = tile['ScheduleInfo']['MaxScheduleDate'], tile['ScheduleInfo']['MinScheduleDate'] 
        date_min, date_max = convert_date(date_start), convert_date(date_finish)
        address = tile['Notice']['PlaceUrl']['Address']
        place = tile['Notice']['PlaceUrl']['Name']
        price = tile['ScheduleInfo']['MinPrice']
        url = tile['Url']
        description = tile['Verdict']
        exhb_data.append({
            'name': name,
            'genre': genre,
            'date_start': date_min,
            'date_finish': date_max,
            'address': address,
            'place': place,
            'price': price,
            'url': url, 
            'description': description
        })
    return exhb_data

if __name__ == "__main__":
    exhibition_lst = get_payload('msk/exhibitions/')['Widget']['CardsCarousels']
    result = collect_exhibitions(exhibition_lst)
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(result)