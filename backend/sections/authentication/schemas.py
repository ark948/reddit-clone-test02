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
    role: Optional[str]
    is_verified: bool
    password_hash: str = Field(exclude=True)
    created_at: datetime
    updated_at: datetime


class UserCreateModel(BaseModel):
    username: str = Field(max_length=16)
    email: str = Field(max_length=42)
    password: str = Field(min_length=6)


class UserLoginModel(BaseModel):
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)


class EmailModel(BaseModel):
    addresses: List[str]


class PasswordResetRequestModel(BaseModel):
    email: str


class PasswordResetConfirmModel(BaseModel):
    new_password: str
    confirm_password: str