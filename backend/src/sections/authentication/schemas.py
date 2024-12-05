import uuid
from datetime import datetime
from typing import (
    List, Optional
)
from pydantic import (
    BaseModel,
    Field
)


class UserModel(BaseModel):
    id: int
    uid: uuid.UUID
    username: str
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    is_verified: bool
    password_hash: str = Field(exclude=True)
    created_at: datetime
    updated_at: datetime


class UserCreateModel(BaseModel):
    username: str = Field(max_length=16)
    email: str = Field(max_length=42)
    password: str = Field(min_length=6)


# auth mechanism
class UserLoginModel(BaseModel):
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)
