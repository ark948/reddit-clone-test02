from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from uuid import UUID


# local imports
from src.sections.database.models import User


class CommunityModelCompact(BaseModel):
    id: int
    title: str


class CommunityMember(BaseModel):
    uid: UUID


class CommunityModel(BaseModel):
    id: int
    title: str
    about: str
    users: Optional[List[CommunityMember]]


class CreateCommunity(BaseModel):
    title: str
    about: str


class CommunityModelForSearch(BaseModel):
    id: int
    title: str
    about: str


class CommunitySearchData(BaseModel):
    title: str