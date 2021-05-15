import html
import random
from typing import List

import discord
import requests
from discord.ext import commands

from lib.emojis import EmojiHelper
from lib.environment import Environment
from lib.netflix_api_util import NetflixAPIUtil
from models.search_response import SearchResponse


class NetflixCog(commands.Cog):

    DEFAULT_SEARCH_LIMIT = 5

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.netflix_util = NetflixAPIUtil()

    @staticmethod
    def __get_templated_embed() -> discord.Embed:
        embed = discord.Embed(color=discord.Color.red())

        embed.set_author(name='YoureMomLole',
                         icon_url='https://www.pngitem.com/pimgs/m/38-381234_download-will-smith-face-image-will-smith-meme.png')

        return embed

    def __get_random_emoji_set(self, guild_id: str) -> List[str]:
        headers = {
            'Authorization': f'Bot {Environment.DISCORD_TOKEN}'
        }

        response = requests.get(url=f'{Environment.DISCORD_API_BASE_URL}/guilds/{guild_id}/emojis', headers=headers)
        emojis = response.json()

        if len(emojis) < self.DEFAULT_SEARCH_LIMIT:
            return EmojiHelper.get_random_sample(self.DEFAULT_SEARCH_LIMIT)

        return random.sample(list(map(lambda e: e.name, emojis)), self.DEFAULT_SEARCH_LIMIT)

    @commands.command(name='search', aliases=['s'])
    async def search(self, ctx, search_query: str):
        try:
            response: SearchResponse = self.netflix_util.search(query=search_query)

            embed: discord.Embed = self.__get_templated_embed()
            embed.set_thumbnail(url=response.results[0].img)

            reacs = self.__get_random_emoji_set(ctx.guild.id)

            for i in range(self.DEFAULT_SEARCH_LIMIT):
                result = response.results[i]
                embed.add_field(name=f'{html.unescape(result.title)} |  Vote with {reacs[i]}',
                                value=result.synopsis,
                                inline=False)

            message: discord.Message = await ctx.send(embed=embed)

            for reac in reacs:
                await message.add_reaction(reac)

        except Exception as e:
            await ctx.send(str(e))


def setup(bot):
    bot.add_cog(NetflixCog(bot))
