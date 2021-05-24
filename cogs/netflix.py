import html
import random
import re
from datetime import datetime
from typing import List

import discord
import requests
from dependency_injector.wiring import Provide
from discord import User
from discord.ext import commands
from discord.ext.commands import Bot, Context

from data.film import Film
from di_container import DIContainer
from lib.emojis import EmojiHelper
from lib.environment import Environment
from lib.parsing_man import ParsingMan
from models.search_response import SearchResponse
from services.film_pool_service import FilmPoolService
from services.netflix_service import NetflixService


class NetflixCog(commands.Cog):

    DEFAULT_SEARCH_LIMIT = 5

    def __init__(self, bot: Bot, netflix_service: NetflixService):
        self.bot: Bot = bot
        self.netflix_service = netflix_service
        self.film_pool_service = FilmPoolService()

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
        films = self.film_pool_service.get_pool()

        embed: discord.Embed = self.__get_templated_embed()

        for film in films:

            film_with_metadata: Film = ParsingMan.parse_film_metadata(film=film)

            voters: List[str] = [
                (await self.bot.fetch_user(user_id=int(vote))).name
                for vote in film_with_metadata.votes
            ]

            embed_description = f'''
            
[Link](https://www.netflix.com/title/{film_with_metadata.id})

Synopsis: {film_with_metadata.synopsis}

Voters: {",".join(voters)}
'''

            # TODO: add film title
            embed.add_field(name=f'{film_with_metadata.title} ({film_with_metadata.year}) | {film_with_metadata.genre}',
                            value=embed_description,
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
            # TODO: get metadata before persisting
            persisted_successfully = self.film_pool_service.add_film_or_vote(film)

            if persisted_successfully:
                await ctx.send(f'Successfully added film with id: {netflix_film_id}')
            else:
                await ctx.send(f'You have already voted this film')

    @commands.command(name='search', aliases=['s'])
    async def search(self, ctx: Context, search_query: str):
        # TODO: ths only works for 1 word search queries unless you use quotes
        # use kwargs instead?
        try:
            response: SearchResponse = self.netflix_service.search(query=search_query,
                                                                   search_limit=self.DEFAULT_SEARCH_LIMIT)

            if len(response.results) == 0:
                await ctx.send(f'No matching results for "{search_query}". Try to change your query.')
                return

            embed: discord.Embed = self.__get_templated_embed()
            embed.set_thumbnail(url=response.results[0].img)

            reacs: List[str] = self.__get_random_emoji_set(ctx.guild.id)
            # TODO: stonky mapping _CHANGE IT_
            reacs_mapped_to_films = dict()
            lower_limit = min(self.DEFAULT_SEARCH_LIMIT, len(response.results))

            for i in range(lower_limit):
                result = response.results[i]
                embed_field_title = f'{html.unescape(result.title)} | Vote with {reacs[i]}'

                embed_description = f'''
[Link](https://www.netflix.com/title/{result.netflix_id})
Synopsis: {html.unescape(result.synopsis)}
'''
                embed.add_field(name=embed_field_title,
                                value=embed_description,
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
            #     self.film_pool_service.add_film(film)

        except Exception as e:
            await ctx.send(str(e))


def setup(bot: Bot, netflix_service: NetflixService = Provide[DIContainer.netflix_service]):
    bot.add_cog(NetflixCog(bot, netflix_service))
