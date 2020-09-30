from bs4 import BeautifulSoup as bs
import urllib.request as urlreq
import urllib.parse as urlparse
import pprint

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

def isCorrectLink(url, category):
    # .../movie/123456/schedule
    responseParams = url.split("/")
    if responseParams[len(responseParams)-2].isdigit():  #проверка ссылок на валидность
        return True
    return False

def getAllLinks(soup): # сортировка ссылок по категориям
    for link in soup.find_all('a', href=True):
        link = 'afisha.ru' + link['href']
        all_links.append(link)
    for link in all_links:
        if  '/movie/' in link:
            if isCorrectLink(link, 'movie/'):
                movie_links.append(link)
        elif '/concert/' in link:
            if isCorrectLink(link, 'concert/'):
               concert_links.append(link)
        elif '/performance/' in link:
            if isCorrectLink(link, 'performance/'):
                performance_links.append(link)
        elif '/exhibition/' in link:
            if isCorrectLink(link, 'exhibition/'):
                exhibition_links.append(link)

    all_categories.append({   # список словарей, разделенный на категории, значение тоже список
        'movie':movie_links,
        'concert': concert_links,
        'performance': performance_links,
        'exhibition': exhibition_links
    })

def getPayload(soup):
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
    
def startWork(url):    
    response = urlreq.urlopen(url)
    soup = bs(response, parser, from_encoding=response.info().get_param('charset'))
    getAllLinks(soup)
    for category in all_categories:
        for lst in category.values():
            for link in lst:
                newRes = urlreq.urlopen('https://' + link)
                soup = bs(newRes, parser)
                getPayload(soup)


if __name__ == "__main__":
    startWork(MAIN_URL)
