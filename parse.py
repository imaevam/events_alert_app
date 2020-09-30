import requests
from bs4 import BeautifulSoup

URL = 'https://www.afisha.ru/msk/schedule_cinema/?view=list'
HEDERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
    'assept': '*/*'
    }
HOST = 'https://www.afisha.ru'

def get_html(url, params=None):
    try:
        r = requests.get(url, headers=HEDERS, params=params)
        r.raise_for_status()
        return r
    except(requests.RequestException, ValueError):
        return False

# собирает список всех ссылок на события с 1 страныцы раздела
def link_dict(html):
    soup = BeautifulSoup(html,'html.parser')
    d_links = []
    for link in soup.find_all('a', class_='new-list__item-link'):
        d_links.append(HOST + link.get('href'))
    return d_links

# pages count
def get_pages_count(html):
    soup = BeautifulSoup(html,'html.parser')
    pages = soup.find_all('a', class_='_3GZQg')
    if pages:
        return int(pages[-1].get_text())
    else:
        return 1

# преобразует ссылки в html data по каждому событию
def events_data(html):
    d = link_dict(html)
    final_data = []
    for link in d:
        ev_kod = get_html(link)
        if ev_kod.status_code == 200:
            final_data.append(get_content(ev_kod.text, link))
        else:
            continue
    return final_data

# преобразует список словарей с html data в список словарей с упорядоченными данными
def get_content(ev_kod, link):
    soup = BeautifulSoup(ev_kod,'html.parser')
    movies = soup.find('div', class_='_21AH_')
    mov_dict = {}
    mov_dict.update({
        'Название': soup.find('div', class_='_3kkV1 dbGiX').get_text(),
        #'Даты': '',
        'Краткое описаие': movies.find('h2', class_='_3X26C').get_text(),
        #'Стоимость': '',
        'Ссылка': link,
    })
    print(mov_dict)
    return mov_dict

def parse():
    html = get_html(URL)
    # print(html.status_code)
    if html.status_code == 200:
        events = []
        p_count = get_pages_count(html.text)
        for page in range(2): #range(1, p_count + 1)
            print(f'Осталось {p_count - page}.', end = "")
            html = get_html(URL, params={'page': page})
            events.extend(events_data(html.text))
        # print(events)
    else:
        print('Error')

if __name__ == '__main__':
    parse()
