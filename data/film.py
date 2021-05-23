from typing import List, Optional

from pydantic import BaseModel


class Film(BaseModel):
    id: str
    discord_user_id: str
    votes: Optional[List[str]]
    date_added: str
