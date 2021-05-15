from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, Field


class Result(BaseModel):
    id: str
    title: str
    img: Optional[str]
    video_type: Optional[str] = Field(alias='vtype')
    netflix_id: Optional[str] = Field(alias='nfid')
    synopsis: Optional[str]
    avg_rating: Optional[Decimal] = Field(alias='avg_rating')
    year: Optional[int]
    runtime: Optional[int]
    imdb_id: Optional[str] = Field(alias='imdbid')
    poster: Optional[str]
    imdb_rating: Optional[str] = Field(alias='imdbrating')
    country_list: Optional[str] = Field(alias='clist')
    title_date: Optional[str] = Field(alias='titledate')


class SearchResponse(BaseModel):
    results: List[Result]
    total: int
    elapse: Decimal

