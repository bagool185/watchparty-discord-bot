from discord.ext import commands

from lib.environment import Environment

client = commands.Bot(command_prefix='#', help_command=None)


@client.event
async def on_ready():
    print('Bot in da house')

extensions = ['cogs.netflix']

[client.load_extension(extension) for extension in extensions]
client.run(Environment.DISCORD_TOKEN)
