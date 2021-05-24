from sys import modules

from discord.ext import commands

from di_container import DIContainer
from lib.environment import Environment

di_container = DIContainer()
di_container.config.from_dict({
    'netflix_api_domain': Environment.NETFLIX_API_DOMAIN,
    'netflix_api_key': Environment.NETFLIX_API_KEY,
    'cosmos_db_domain': Environment.COSMOS_DB_HOST,
    'cosmos_db_key': Environment.COSMOS_DB_KEY
})

di_container.wire(modules=[modules[__name__]])

client = commands.Bot(command_prefix='#', help_command=None)
extensions = ['cogs.netflix']

[client.load_extension(extension) for extension in extensions]
client.run(Environment.DISCORD_TOKEN)



