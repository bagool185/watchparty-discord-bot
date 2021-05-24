import requests

from lib.environment import Environment
from models.search_response import SearchResponse


class NetflixService:

    def __init__(self, domain: str, api_key: str):
        self.base_url = f'https://{domain}'

        self.headers = {
            'x-rapidapi-key': Environment.NETFLIX_API_KEY,
            'x-rapidapi-host': domain
        }

    def search(self, query: str, search_limit: int) -> SearchResponse:
        query_params = {
            'limit': str(search_limit),
            'countryList': Environment.UK_CODE,
            'query': query
        }

        raw_response = requests.get(url=f'{self.base_url}/search', headers=self.headers, params=query_params)
        search_response = SearchResponse.parse_raw(raw_response.text)

        return search_response
