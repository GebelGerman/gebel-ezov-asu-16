from bs4 import BeautifulSoup
from urllib.request import Request, urlopen


url = "https://videomore.ru/films/komediya"


def get_html(url):
    req = Request(url)
    html = urlopen(req).read()
    return html

def parse(soup, index):#сделать генератор
    table = soup.find(class_="project_vertical_list")
    row = table.find_all(class_="project_vertical_item")[index]
    name = row.find(class_='pvi-title')
    a = row.find(class_='pvi-description').text.split('\n')
    film = {
        'Название': name.text,
        'Жанр': a[1],
        'Год': a[2],
        'Страна': a[3]
    }
    return film

def main():
    soup = BeautifulSoup(get_html(url), "html.parser")
    for i in range(1,10):
        print('----------------------------')
        print(parse(soup,i))


if __name__ == "__main__":
    main()
