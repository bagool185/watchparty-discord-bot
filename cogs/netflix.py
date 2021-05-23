import html
import random
import re
from datetime import datetime
from typing import List

import discord
import requests
from discord import User
from discord.ext import commands
from discord.ext.commands import Bot, Context

from data.db_util import DBUtil
from data.film import Film
from lib.emojis import EmojiHelper
from lib.environment import Environment
from lib.netflix_api_util import NetflixAPIUtil
from models.search_response import SearchResponse


class NetflixCog(commands.Cog):

    DEFAULT_SEARCH_LIMIT = 5

    def __init__(self, bot):
        self.bot: Bot = bot
        self._last_member = None
        self.netflix_util = NetflixAPIUtil()
        self.db_util = DBUtil()

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

    @commands.command(name='get', aliases=['g'])
    async def get(self, ctx: Context):
        # TODO: order by number of votes (desc)
        films = self.db_util.get_pool()

        embed: discord.Embed = self.__get_templated_embed()

        for film in films:

            voters: List[str] = [(await self.bot.fetch_user(user_id=int(vote))).name for vote in film.votes]
            # TODO: add film title
            embed.add_field(name=f'https://www.netflix.com/title/{film.id}',
                            value=f'Voters: {",".join(voters)}',
                            inline=False)

        await ctx.send(embed=embed)

    @commands.command(name='add', aliases=['a'])
    async def add(self, ctx: Context, netflix_link: str):
        pattern = r'(https:\/\/www.netflix.com\/(browse\?jbv=|title\/))(\d+)'
        matches = re.match(pattern, netflix_link)

        if matches:
            netflix_film_id = matches.groups()[-1]
            user: User = ctx.author
            utc_datetime_now: str = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

            film = Film(
                id=netflix_film_id,
                discord_user_id=user.id,
                date_added=utc_datetime_now,
                votes=[user.id]
            )

            self.db_util.add_film_or_vote(film)

    @commands.command(name='search', aliases=['s'])
    async def search(self, ctx: Context, search_query: str):
        try:
            response: SearchResponse = self.netflix_util.search(query=search_query)

            embed: discord.Embed = self.__get_templated_embed()
            embed.set_thumbnail(url=response.results[0].img)

            reacs: List[str] = self.__get_random_emoji_set(ctx.guild.id)
            # TODO: stonky mapping _CHANGE IT_
            reacs_mapped_to_films = dict()

            for i in range(self.DEFAULT_SEARCH_LIMIT):
                result = response.results[i]
                embed.add_field(name=f'{html.unescape(result.title)} |  Vote with {reacs[i]}',
                                value=result.synopsis,
                                inline=False)

                reacs_mapped_to_films[reacs[i]] = result.netflix_id

            message: discord.Message = await ctx.send(embed=embed)

            for reac in reacs:
                await message.add_reaction(reac)

            # # TODO: this obscenity
            # while True:
            #     reaction, reaction_user = await self.bot.wait_for('reaction_add')
            #     netflix_film_id: str = reacs_mapped_to_films[reaction]
            #     utc_datetime_now: str = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
            #
            #     film: Film = Film(netflix_id=netflix_film_id,
            #                       discord_user_id=reaction_user,
            #                       date_added=utc_datetime_now)
            #
            #     self.db_util.add_film(film)

        except Exception as e:
            await ctx.send(str(e))


def setup(bot):
    bot.add_cog(NetflixCog(bot))
