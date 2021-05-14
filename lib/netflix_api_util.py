import http.client

from lib.environment import Environment


class NetflixAPIUtil:

    def __init__(self):
        self.http_client = http.client.HTTPSConnection(Environment.NETFLIX_API_BASE_URL)

    def __del__(self):
        self.http_client.close()
