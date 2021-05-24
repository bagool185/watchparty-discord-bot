import sys

from azure.cosmos import CosmosClient
from dependency_injector import containers, providers
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration, DependenciesContainer

from lib.environment import Environment
from services.film_pool_service import FilmPoolService
from services.netflix_service import NetflixService


class ConfigContainer(DeclarativeContainer):
    config = Configuration('config')


class DIContainer(containers.DeclarativeContainer):

    root = DependenciesContainer(config=Configuration())
    config = providers.Configuration()


    netflix_service = providers.Factory(
        NetflixService,
        domain=config.netflix_api_domain,
        api_key=config.netflix_api_key
    )

    cosmos_client = providers.Singleton(
        CosmosClient,
        domain=config.cosmos_db_domain,
        credential=config.cosmos_db_key
    )

    film_pool_service = providers.Factory(
        FilmPoolService,
        cosmos_client=cosmos_client
    )


def init_di_container():
    di_container = DIContainer(
        root=ConfigContainer(
            # TODO: these aren't being set at all?
            config={
                'netflix_api_domain': Environment.NETFLIX_API_DOMAIN,
                'netflix_api_key': Environment.NETFLIX_API_KEY,
                'cosmos_db_domain': Environment.COSMOS_DB_HOST,
                'cosmos_db_key': Environment.COSMOS_DB_KEY
            }
        )
    )

    di_container.wire(modules=[sys.modules[__name__]])
