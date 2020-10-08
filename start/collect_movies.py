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
     

def collect_movies(movie_lst): 
    movie_data = [] 
    tiles = [tile for item in movie_lst for tile in item['Tiles']]
    for tile in tiles:
        name = tile['Name']
        genre = tile['Badge']
        date_start, date_finish = tile['ScheduleInfo']['MaxScheduleDate'], tile['ScheduleInfo']['MinScheduleDate'] 
        date_min, date_max = convert_date(date_start), convert_date(date_finish)
        place = tile['Notice']['PlaceUrl']['Name']
        price = tile['ScheduleInfo']['MinPrice']
        url = tile['Url']
        description = tile['Verdict']
        movie_data.append({
            'name': name,
            'genre': genre,
            'date_start': date_min,
            'date_finish': date_max,
            'place': place,
            'price': price,
            'url': url, 
            'description': description
        })
    return movie_data

if __name__ == "__main__":
    movie_lst = get_payload('msk/cinema')['Widget']['CardsCarousels']
    result = collect_movies(movie_lst)
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(result)
