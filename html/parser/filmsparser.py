from bs4 import BeautifulSoup
from urllib.request import Request, urlopen


url = "https://videomore.ru/films/komediya"


def get_html(url):
    req = Request(url)
    html = urlopen(req).read()
    return html

def parse(html):#сделать генератор
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find(class_="project_vertical_list")
    films = []
    for row in table.find_all(class_="project_vertical_item"):
        name = row.find(class_='pvi-title')
        description = row.find(class_='pvi-description')
        text = str(description.text)
        a = text.split('\n')
        films.append({
            'Название': name.text,
            'Жанр': a[1],
            'Год': a[2],
            'Страна': a[3]
        })
    return films

def main():
    films = parse(get_html(url))
    for film in films:
        print('----------')
        print(film)     

if __name__ == "__main__":
    main()
