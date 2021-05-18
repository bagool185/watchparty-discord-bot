from typing import Optional

import azure.cosmos.exceptions
from azure.cosmos import ContainerProxy, CosmosClient, DatabaseProxy, PartitionKey

from data.film import Film
from lib.environment import Environment


class DBUtil:

    def __init__(self):
        self.cosmos_client = CosmosClient(url=Environment.COSMOS_DB_HOST,
                                          credential=Environment.COSMOS_DB_KEY)
        self.container: Optional[ContainerProxy] = None

        self.__initialise_container()

    @staticmethod
    def __get_partition_key(film: Film) -> str:
        return f'{film.discord_user_id}/{film.netflix_id}'

    def __initialise_container(self):
        database_client: DatabaseProxy = self.cosmos_client.get_database_client(Environment.DB_NAME)
        self.container: ContainerProxy = database_client.create_container_if_not_exists(
            id=Environment.CONTAINER_NAME,
            partition_key=PartitionKey(path='/discordUserId'),
            offer_throughput=400
        )

    def get_film(self, film: Film) -> Optional[Film]:

        try:
            item_response = self.container.read_item(item=film.netflix_id,
                                                     partition_key=self.__get_partition_key(film))

            return item_response
        except azure.cosmos.exceptions.CosmosHttpResponseError as e:
            if e.status_code == 404:
                # item not found, cosmos throws 404 cause yes
                return None

            raise e

    def add_film(self, film: Film):

        item_response: Optional[Film] = self.get_film(film)

        if item_response is None:
            self.container.create_item(film)
        else:
            item_response.votes = item_response.votes + 1
            self.container.upsert_item(film)

