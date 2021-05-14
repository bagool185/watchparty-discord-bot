import discord

from lib.environment import Environment

client = discord.Client()


@client.event
async def on_ready():
    pass


client.run(Environment.DISCORD_TOKEN)
