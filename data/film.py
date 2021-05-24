from typing import List, Optional

from pydantic import BaseModel


# TODO: add guild id?
class Film(BaseModel):
    id: str
    discord_user_id: str
    votes: Optional[List[str]]
    date_added: str
    title: Optional[str]
    synopsis: Optional[str]
    genre: Optional[str]
    year: Optional[str]
