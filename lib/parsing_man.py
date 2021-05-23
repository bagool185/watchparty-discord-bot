from typing import Optional

import requests

from bs4 import BeautifulSoup

from data.film import Film


class ParsingMan:

    @staticmethod
    def parse_film_metadata(film: Film) -> Optional[Film]:
        url = f'https://www.netflix.com/gb/title/{film.id}'

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0'
        }

        response = requests.get(url=url, headers=headers)

        if response.status_code == 200:

            soup: BeautifulSoup = BeautifulSoup(response.content, 'html.parser')
            title_info_elem = soup.select_one('div.title-info')

            film.title = title_info_elem.select_one(selector='h1.title-title').text.strip()
            film.synopsis = title_info_elem.select_one(selector='div.title-info-synopsis').text.strip()
            film.year = title_info_elem.select_one(selector='span.title-info-metadata-item.item-year').text.strip()
            film.genre = title_info_elem.select_one(selector='a.title-info-metadata-item.item-genre').text.strip()

            return film

        return None
