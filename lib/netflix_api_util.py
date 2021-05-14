import requests

from lib.environment import Environment
from models.search_response import SearchResponse


class NetflixAPIUtil:

    def __init__(self):
        self.base_url = f'https://{Environment.NETFLIX_API_DOMAIN}'

        self.headers = {
            'x-rapidapi-key': Environment.NETFLIX_API_KEY,
            'x-rapidapi-host': Environment.NETFLIX_API_DOMAIN
        }

    def search(self, query: str) -> SearchResponse:

        query_params = {
            'limit': '5',
            'countryList': Environment.UK_CODE,
            'query': query
        }

        raw_response = requests.get(url=f'{self.base_url}/search', headers=self.headers, params=query_params)
        search_response = SearchResponse.parse_raw(raw_response.text)

        return search_response
