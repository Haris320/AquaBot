import requests
from bs4 import BeautifulSoup
from pytmangadex import Mangadex

mangadex = Mangadex()
global wishlist
wishlist = {}


def genre(a):
    a = a.lower()
    b = {
        'action': 2,
        'adventure': 3,
        'comedy': 5,
        'drama': 8,
        'fantasy': 10,
        'historical': 13,
        'horror': 14,
        'mystery': 20,
        'romance': 23,
        'sci-fi': 25,
    }
    value = b.get(a)
    if value is None:
        return 999
    return b.get(a)


def get_id(category, pos):
    r = requests.get('https://mangadex.org/genre/' + category)
    soup = BeautifulSoup(r.text, 'html.parser')
    results = soup.find_all('div', attrs={'class': 'manga-entry col-lg-6 border-bottom pl-0 my-1'})
    first_result = results[pos]
    url = first_result.find('a')['href']
    return url[7:12]


async def search_links(term: str):
    a = []
    mangadex.login("Parrota", "QWERTY1234", newLogin=True)
    async for manga in mangadex.search(term, 10):
        a.append(f"https://mangadex.org/title/{manga.manga_id}/")
    return a


async def search_titles(term: str):
    a = []
    mangadex.login("Parrota", "QWERTY1234", newLogin=True)
    async for manga in mangadex.search(term, 10):
        a.append(manga.title)
    return a


def get_description(url: str):
    id = url[7:12]
    description = mangadex.get_manga(int(id)).description
    return description


"""def getImage(id):
# r = requests.get('https://mangadex.org/'+id+)
soup = BeautifulSoup(r.text, 'html.parser')
results = soup.find_all('div', attrs={'class': 'manga-entry col-lg-6 border-bottom pl-0 my-1'})
first_result = results[pos]
url = first_result.find('a')['href']
return url[7:12]"""
