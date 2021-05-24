from dependency_injector import containers, providers
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration, DependenciesContainer

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
