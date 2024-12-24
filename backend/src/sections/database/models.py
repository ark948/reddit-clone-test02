import uuid
from datetime import datetime
from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.types import Text
from sqlalchemy import ForeignKey
from typing import (
    Optional, List
)
from sqlmodel import (
    SQLModel, Field, Column, Relationship
)

class UserCommunity(SQLModel, table=True):
    user_id: int = Field(default=None, foreign_key="users.id", primary_key=True)
    community_id: int = Field(default=None, foreign_key="communities.id", primary_key=True)

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int = Field(primary_key=True)
    uid: uuid.UUID = Field(sa_column=Column(pg.UUID, nullable=False, default=uuid.uuid4))
    username: str = Field(unique=True, nullable=False)
    email: str = Field(unique=True, nullable=False)
    role: str = Field(sa_column=Column(pg.VARCHAR, nullable=False, server_default="user"))
    is_verified: bool = Field(default=False)
    password_hash: str = Field(exclude=True)
    communities: List["Community"] = Relationship(
        link_model=UserCommunity,
        back_populates="users",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    posts: List["Post"] = Relationship(back_populates="owner", sa_relationship_kwargs={"lazy": "selectin"})
    profile_id: Optional[int] = Field(default=None, foreign_key="profiles.id")
    profile: Optional["Profile"] = Relationship(back_populates="user")
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

    def __repr__(self):
        return f'<User {self.username}>'
    

class Community(SQLModel, table=True):
    __tablename__ = "communities"

    id: int = Field(primary_key=True)
    title: str = Field(nullable=False)
    about: str = Field(nullable=False)
    users: List["User"] = Relationship(
        link_model=UserCommunity,
        back_populates="communities",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    posts: List["Post"] = Relationship(back_populates="community", sa_relationship_kwargs={"lazy": "selectin"})



class Post(SQLModel, table=True):
    __tablename__ = "posts"

    id: int = Field(primary_key=True)
    title: str = Field(nullable=False)
    body: str = Field(nullable=False) # update this later
    reactions: int = Field(default=0, nullable=False)
    owner: User = Relationship(back_populates="posts")
    owner_id: int = Field(default=None, foreign_key="users.id")
    community: Community = Relationship(back_populates="posts")
    community_id: int = Field(default=None, foreign_key="communities.id")
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))


class Profile(SQLModel, table=True):
    __tablename__ = "profiles"
    
    id: int = Field(primary_key=True)
    first_name: str = Field(nullable=True)
    last_name: str = Field(nullable=True)
    karma: int = Field(default=0)
    user: Optional["User"] = Relationship(
        sa_relationship_kwargs={"uselist": False},
        back_populates="profile"
    )

    @property
    def get_related_user(self):
        return self.user
