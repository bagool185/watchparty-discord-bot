import sys

from dependency_injector.wiring import Provide, inject
from discord.ext import commands

from di_container import ConfigContainer, DIContainer
from lib.environment import Environment
from services.netflix_service import NetflixService


@inject
def main(netflix_service: NetflixService = Provide[DIContainer.netflix_service]):
    client = commands.Bot(command_prefix='#', help_command=None)

    @client.event
    async def on_ready():
        print('Bot in da house')

    extensions = ['cogs.netflix']

    [client.load_extension(extension) for extension in extensions]
    client.run(Environment.DISCORD_TOKEN)


if __name__ == '__main__':

    di_container = DIContainer(
        root=ConfigContainer(
            config={
                'netflix_api_domain': Environment.NETFLIX_API_DOMAIN,
                'netflix_api_key': Environment.NETFLIX_API_KEY
            }
        )
    )

    di_container.wire(modules=[sys.modules[__name__]])

    main()
