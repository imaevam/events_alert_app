import requests
from bs4 import BeautifulSoup as bs
import urllib.request as urlreq
import urllib.parse as urlparse

all_links = []
movie_links = []
concert_links = []
performance_links = []
exhibition_links = []
all_categories = []
parser = 'html.parser'
MAIN_URL = "https://afisha.ru"

# в концертах и спектаклях много повторов
# поправить заголовки
# Галерея фото -> byte подумать как передать картинки?

def check_links(url, category): # .../movie/123456/
    response_params = url.split("/")
    if response_params[-2].isdigit():  #проверка ссылок на валидность
        return True
    return False

def collect_links(soup): # сортировка ссылок по категориям
    for link in soup.find_all('a', href=True):
        url = link['href']
        link = f'afisha.ru{url}'
        all_links.append(link)
    for link in all_links:
        if '/movie/' in link:
            if check_links(link, 'movie/'):
                movie_links.append(link)
        elif '/concert/' in link:
            if check_links(link, 'concert/'):
               concert_links.append(link)
        elif '/performance/' in link:
            if check_links(link, 'performance/'):
                performance_links.append(link)
        elif '/exhibition/' in link:
            if check_links(link, 'exhibition/'):
                exhibition_links.append(link)

    all_categories.append({   # список словарей, разделенный на категории, значение тоже список
        'movie': movie_links,
        'concert': concert_links,
        'performance': performance_links,
        'exhibition': exhibition_links
    })

def get_payload(soup):
    months = soup.find_all('div', {'class': 'calendar-simple__month'})
    print(months)
    #title = soup.find_all('h1').text  Как достать заголовок? 
    notice = soup.find_all('h2')[1].text
    print(notice)
    text = soup.find_all('p')[0].text
    print(text)
    contents = soup.find_all('div', {'class': 'content_view_list'})
    try: # опционально для каждой категории
        for content in contents:
            lis = content.find_all('li', {'class': 'unit__schedule-row'})
            for li in lis:
                place = li.find('a', {'class': 'unit__movie-name__link'}).text
                sessions = li.find_all('li', {'class': 'timetable__item'})
                for session in sessions:
                    time = session.find('time', {'class': 'timetable__item-time'}).text
                    price = session.find('span', {'class': 'timetable__item-price'}).text
                print(f'В {place} в {time} {price}')
    except (UnboundLocalError, ValueError, AttributeError):
        print("None")
    
def start_work(url):    
    response = urlreq.urlopen(url)
    soup = bs(response, parser, from_encoding=response.info().get_param('charset'))
    collect_links(soup)
    for category in all_categories:
        for lst in category.values():
            for link in lst:
                new_response = urlreq.urlopen('https://' + link)
                soup = bs(new_response, parser)
                get_payload(soup)

if __name__ == "__main__":
    start_work(MAIN_URL)
