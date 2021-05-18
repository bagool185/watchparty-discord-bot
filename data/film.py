from typing import Optional

from pydantic import BaseModel


class Film(BaseModel):
    netflix_id: str
    discord_user_id: str
    votes: Optional[int]
    date_added: str

