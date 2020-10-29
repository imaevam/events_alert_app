import requests

from flask import current_app
from bs4 import BeautifulSoup

from webapp.model import db, Event


url = current_app.config['URL']
heders = current_app.config['HEDERS']
host = current_app.config['HOST']

event_list = ['schedule_cinema/'] #'schedule_concert/',


def get_html(url, params=''):
    try:
        #r = requests.get(url, headers={'Accept': 'application/json'}).json()
        r = requests.get(url, headers=heders, params=params)
        r.raise_for_status()
        return r
    except(requests.RequestException, ValueError):
        print('Сетевая ошибка')
        return False

# собирает список всех ссылок на события с 1 страныцы раздела
def link_dict(html):
    soup = BeautifulSoup(html,'html.parser')
    d_links = []
    for link in soup.find_all('a', class_='_1F19s'):
        d_links.append(host + link.get('href'))
    return d_links

# pages count
def get_pages_count(html):
    soup = BeautifulSoup(html,'html.parser')
    pages = soup.find_all('a', class_='_3GZQg')
    if pages:
        if int(pages[-1].get_text()) < 5:   # концерты и театр - 52 и 76 стр. (очень долго)
            return int(pages[-1].get_text())
        else:
            return 5
    else:
        return 1

# преобразует ссылки в html data по каждому событию
def events_data(html):
    d = link_dict(html)
    final_data = []
    for link in d:
        ev_kod = get_html(link)
        if ev_kod.status_code == 200:
            get_content(ev_kod.text, link)
            final_data.append(get_content(ev_kod.text, link))
        else:
            return {0: 0}
    #print(final_data)
    return final_data

def is_desc(value):
    if value is None:
        return '-'
    else:
        return value

# преобразует список словарей с html data в список словарей с упорядоченными данными
def get_content(ev_kod, link):
    soup = BeautifulSoup(ev_kod,'html.parser')
    movie = soup.find('section', class_='_XY8-')
    mov_dict = {}
    title = soup.find('div', class_='_3kkV1 dbGiX').get_text()
    description = '-'
    soup.find('div', class_='_3kkV1 dbGiX').get_text()
    if is_desc(soup.find('h2', class_='_3X26C')) != None:
        try:
            description = is_desc(soup.find('h2', class_='_3X26C')).get_text()
        except(AttributeError):
            description = '-'
    seve_data(title, description, link)
    '''
    mov_dict.update({
        'title': title,
        #'Даты': movie.find('div', class_='dxtuN').get_text(', ').split(),
        # список резать по "России" и брать 3 первых элемента
        'description': description,
        #'Стоимость': '',
        'url': link,
    })
    return mov_dict
    '''
    

def parse():
    for catgory in event_list:
        url_category = url + catgory
        html = get_html(url_category)
        #print(html.status_code)
        if html.status_code == 200:
            events = []
            p_count = get_pages_count(html.text)
            for page in range(1, p_count + 1):
                #print(f'Обработка данных: {p_count - page}.', end = "")
                url_page = url_category + 'page' + str(page)
                #print(url_page)
                html = get_html(url_page)
                events.extend(events_data(html.text))
            
            return events
            
        else:
            print('Error')


def seve_data(title, description, link):
    #event_exists = Event.query.filter(Event.link = link).count()
    #if not event_exists:
    save_event = Event(title=title, description=description, link=link)
    db.session.add(save_event)
    db.session.commit()
'''
if __name__ == '__main__':
    parse()
'''
