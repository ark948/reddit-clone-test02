from pydantic import BaseModel
from datetime import datetime


from src.sections.database.models import User


class PostModel(BaseModel):
    id: int
    title: str
    body: str
    owner_id: int
    created_at: datetime
    updated_at: datetime


class CreatePost(BaseModel):
    title: str
    body: str