from pydantic import BaseModel
from typing import (
    Optional
)



class ProfileModel(BaseModel):
    id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    karma: int = 0


class CreateProfileModel(BaseModel):
    user_id: int


class ProfileFromUser(BaseModel):
    id: int
    username: str
    email: str
    role: Optional[str]
    is_verified: bool
    profile: Optional[ProfileModel]


class UpdateProfile(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None