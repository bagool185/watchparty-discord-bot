import requests

from lib.environment import Environment
from models.search_response import SearchResponse


class NetflixAPIUtil:

    def __init__(self):
        self.http_client = http.client.HTTPSConnection(Environment.NETFLIX_API_BASE_URL)
        self.headers = {
            'x-rapidapi-key': Environment.NETFLIX_API_KEY,
            'x-rapidapi-host': Environment.NETFLIX_API_BASE_URL
        }

    def search(self, query: str) -> SearchResponse:
        self.http_client.request(method="GET", headers=self.headers, url=f'/aaapi.cgi?q={query}')
        res = self.http_client.getresponse()
        search_response = SearchResponse.parse_raw(res.read().decode('utf-8'))

        return search_response

    def __del__(self):
        self.http_client.close()
