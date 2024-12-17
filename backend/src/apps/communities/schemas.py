from pydantic import BaseModel, ConfigDict
from typing import List, Optional


# local imports
from src.sections.database.models import User


class CommunityModel(BaseModel):
    id: int
    title: str
    about: str
    users: Optional[List[User]]



class CreateCommunity(BaseModel):
    title: str
    about: str