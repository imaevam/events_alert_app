import json
import requests
import pprint


def get_payload(url):
    url = f"https://afisha.ru/{url}"
    return requests.get(url=url, headers={'Accept': 'application/json'}).json()

def collect_concerts(concert_lst):
    concerts_data = [] 
    tiles = [tile for item in concert_lst for tile in item['Tiles']]
    for tile in tiles:
        name = tile['Name']
        genre = tile['Badge']
        date = tile['Notice']['Notice']
        address = tile['Notice']['PlaceUrl']['Address']
        place = tile['Notice']['PlaceUrl']['Name']
        price = tile['ScheduleInfo']['MinPrice']
        url = tile['Url']
        description = tile['Verdict']
        concerts_data.append({
            'name': name,
            'genre': genre,
            'date': date,
            'address': address,
            'place': place,
            'price': price,
            'url': url, 
            'description': description
        })
    return concerts_data

if __name__ == "__main__":
    concert_lst = get_payload('msk/concerts/')['Widget']['CardsCarousels']
    result = collect_concerts(concert_lst)
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(result)

