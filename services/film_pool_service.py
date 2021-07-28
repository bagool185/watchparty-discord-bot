from typing import List, Optional

import azure.cosmos.exceptions
from azure.core.exceptions import ServiceRequestError
from azure.cosmos import ContainerProxy, CosmosClient, DatabaseProxy, PartitionKey

from data.film import Film
from lib.environment import Environment


class FilmPoolService:

    def __init__(self):
        try:
            self.cosmos_client = CosmosClient(url=Environment.COSMOS_DB_HOST,
                                              credential=Environment.COSMOS_DB_KEY)
            self.container: Optional[ContainerProxy] = None

            self.__initialise_container()
        except azure.cosmos.exceptions.CosmosResourceNotFoundError as e:
            print(f'''
Couldn\'t connect to CosmosDB. Check your connection string
Host:"{Environment.COSMOS_DB_HOST}"
Stack trace:\n {e}'''
                  )

            exit(1)

    def __initialise_container(self):
        database_client: DatabaseProxy = self.cosmos_client.get_database_client(Environment.DB_NAME)
        self.container: ContainerProxy = database_client.create_container_if_not_exists(
            id=Environment.CONTAINER_NAME,
            partition_key=PartitionKey(path='/discord_user_id'),
            offer_throughput=400
        )

    def get_pool(self) -> List[Film]:
        item_responses: List[dict] = list(self.container.read_all_items(max_item_count=10))

        films: List[Film] = [Film.parse_obj(item_response) for item_response in item_responses]

        return films

    def get_film(self, film: Film) -> Optional[Film]:

        try:
            item_response: dict = self.container.read_item(item=film.id,
                                                           partition_key=film.discord_user_id)

            return Film.parse_obj(item_response)
        except azure.cosmos.exceptions.CosmosHttpResponseError as e:
            if e.status_code == 404:
                # item not found, cosmos throws 404 cause yes
                return None

            raise e

    def add_film_or_vote(self, film: Film) -> bool:

        item_response: Optional[Film] = self.get_film(film)

        if item_response is None:
            self.container.create_item(body=film.dict())
            return True
        else:
            # only add vote if it doesn't already exist TODO: this is questionable at best
            if film.discord_user_id not in item_response.votes:
                item_response.votes.append(film.discord_user_id)
                self.container.upsert_item(item_response.dict())

                return True

        return False


