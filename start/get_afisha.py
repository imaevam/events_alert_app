import requests
from bs4 import BeautifulSoup as bs

#функция с requests

def nearest_events(html):
    soup = bs(html, 'html.parser')
    all_events = soup.find('div', class_='filtered-content__content') # список, где все события на ближайшее время
    all_events = all_events.find_all('a', class_='tile__link')
    result_events = []
    for events in all_events:
        genre = events.find(class_='tile__badge').text
        title = events.find('h2').text
        url = events.get('href')
        description = events.find('p').text
        result_events.append({
            'genre': genre, 
            'title': title,
            'url': url, 
            'description': description
        })
    print(result_events)

if __name__ == "__main__":
    html = get_html('https://afisha.ru')
    if html:
        nearest_events(html)

        #как я поняла, дату и цену можно достать у каждого события, если пройти по каждой ссылке по отдельности. Может можно как-то по-другому?
