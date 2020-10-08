import json
import requests
import pprint

def get_payload(url):
    url = f"https://afisha.ru/{url}"
    return requests.get(url=url, headers={'Accept': 'application/json'}).json()

def convert_date(date):
    date = str(date)
    out = date.replace("T"," ")
    return out

def collect_plays(theatre_lst): 
    theatre_data = [] 
    tiles = [tile for item in theatre_lst for tile in item['Tiles']]
    for tile in tiles:
        name = tile['Name']
        genre = tile['Badge']
        date_max = tile['ScheduleInfo']['MaxScheduleDate'] 
        date = convert_date(date_max)
        address = tile['Notice']['PlaceUrl']['Address']
        place = tile['Notice']['PlaceUrl']['Name']
        price = tile['ScheduleInfo']['MinPrice']
        url = tile['Url']
        description = tile['Verdict']
        theatre_data.append({
            'name': name,
            'genre': genre,
            'date': date,
            'address': address,
            'place': place,
            'price': price,
            'url': url, 
            'description': description
        })
    return theatre_data

if __name__ == "__main__":
    theatre_lst = get_payload('msk/theatre/')['Widget']['CardsCarousels']
    result = collect_plays(theatre_lst)
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(result)
