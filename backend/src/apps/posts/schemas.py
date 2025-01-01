from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime


from src.sections.database.models import User, Comment


class PostModel(BaseModel):
    id: int
    title: str
    body: str
    reactions: int
    owner_id: int
    community_id: int
    created_at: datetime
    updated_at: datetime


class PostWithComments(BaseModel):
    id: int
    title: str
    body: str
    reactions: int
    owner_id: int
    community_id: int
    comments: Optional[List[Comment]] = None
    created_at: datetime
    updated_at: datetime


class CreatePost(BaseModel):
    title: str
    body: str


class UpdatePost(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None