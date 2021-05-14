from decimal import Decimal
from typing import List

from pydantic import BaseModel, Field


class Result(BaseModel):
    id: str
    title: str
    img: str
    video_type: str = Field(alias='vtype')
    netflix_id: str = Field(alias='nfid')
    synopsis: str
    avg_rating: Decimal = Field(alias='avg_rating')
    year: int
    runtime: int
    imdb_id: str = Field(alias='imdbid')
    poster: str
    imdb_rating: str = Field(alias='imdbrating')
    country_list: str = Field(alias='clist')
    title_date: str = Field(alias='titledate')


class SearchResponse(BaseModel):
    results: List[Result]
    total: int
    elapse: Decimal

