import requests
import re
from bs4 import BeautifulSoup

class Response:
    def __init__(self, headers, manga, curr_page=1):
        self.headers = headers
        self.manga = manga
        self.curr_page = curr_page
        self.webpage_url = 'http://www.mangareader.net/{}/{}/{}'.format(self.manga.formatted_manga_name,
                                                                        str(self.manga.start),
                                                                        str(self.curr_page))
        self.response_text = requests.get(self.webpage_url, headers=self.headers).text
        self.soup = BeautifulSoup(self.response_text, 'lxml')
        self.last_page = int(
                re.search('\s\d+', str([x.text for x in self.soup.findAll('div', {'id': 'selectpage'})])).group(
                    0).strip(' '))
        # url came with some weird formatting, this is the fix
        self.img_location = str([x['src'] for x in self.soup.findAll('img', {'id': 'img'})]).translate({ord(x): None for x in "'[]"})
        self.img = requests.get(self.img_location).content
        # mangareader has 1 img on each page (the manga), may cause issues later
        self.img_src = self.soup.find('img')['src']
        self.img_resp = requests.get(self.img_src, stream=True, headers=self.headers)
