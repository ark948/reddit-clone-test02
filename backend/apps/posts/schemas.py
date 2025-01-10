from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime


from backend.sections.database.models import (
    User, 
    Comment, 
    Tag
)


class PostModel(BaseModel):
    id: int
    title: str
    body: str
    reactions: int
    owner_id: int
    community_id: int
    created_at: datetime
    updated_at: datetime


class PostWithTags(BaseModel):
    id: int
    title: str
    body: str
    reactions: int
    owner_id: int
    community_id: int
    tags: Optional[List[Tag]]
    created_at: datetime
    updated_at: datetime


class PostWithTagsAndComments(BaseModel):
    id: int
    title: str
    body: str
    reactions: int
    owner_id: int
    community_id: int
    tags: Optional[List[Tag]]
    comments: Optional[List[Comment]]
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


class PostsWithCertainTags(BaseModel):
    title: str
    body: str


class CreatePost(BaseModel):
    title: str
    body: str


class UpdatePost(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None