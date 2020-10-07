import json
import requests
import pprint

cur_dir = "/Users/aleksejfilippov/Desktop/Python_projects/images/"

def get_payload(url):
    url = f"https://afisha.ru/{url}"
    with requests.get(url=url, headers={'Accept': 'application/json'}) as response:
        return json.loads(response.text)

def save_img(url, path_to_save, movie_id):
    if not os.path.exists(path_to_save):
        os.mkdir(path_to_save)

    image_name = url.split('/')[-1]
    img_data = requests.get(url).content
    save_name = os.path.join(path_to_save, movie_id + "__" + image_name)
    with open(save_name, 'wb') as handler:
        handler.write(img_data)
    return save_name

def collect_concerts(concert_lst):
    concerts_data = [] 
    for cns in concert_lst:
        name = cns['Tile']['Name']
        genre = cns['Tile']['Badge']
        date = cns['Tile']['Notice']['Notice']
        place = cns['Tile']['Notice']['PlaceUrl']['Name']
        address_place = cns['Tile']['Notice']['PlaceUrl']['Address']
        price = cns['Tile']['ScheduleInfo']['MinPrice']
        url = cns['Tile']['Url']
        description = cns['Tile']['Verdict']
        concerts_data.append({
            'name':name,
            'genre': genre,
            'date': date,
            'place': place,
            'address_place': address_place,
            'price': price,
            'url': url,
            'description': description

            })
    return concerts_data


if __name__ == "__main__":
    concert_lst = get_payload('msk/concerts/')['Widget']['Tiles']
    result = collect_concerts(concert_lst)
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(result)

