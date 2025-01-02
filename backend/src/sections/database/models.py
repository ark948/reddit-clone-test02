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


class PostTag(SQLModel, table=True):
    post_id: int = Field(default=None, foreign_key="posts.id", primary_key=True)
    tag_id: int = Field(default=None, foreign_key="tags.id", primary_key=True)


class Like(SQLModel, table=True):
    __tablename__ = "likes"

    id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="users.id", nullable=False)
    post_id: int = Field(foreign_key="posts.id", nullable=False)


class Dislike(SQLModel, table=True):
    __tablename__ = "dislikes"

    id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="users.id", nullable=False)
    post_id: int = Field(foreign_key="posts.id", nullable=False)


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
    comments: List["Comment"] = Relationship(back_populates="author", sa_relationship_kwargs={"lazy": "selectin"})
    profile_id: Optional[int] = Field(default=None, foreign_key="profiles.id")
    profile: Optional["Profile"] = Relationship(back_populates="user")
    likes: List["Post"] = Relationship(
        link_model=Like,
        back_populates="liked_by",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    dislikes: List["Post"] = Relationship(
        link_model=Dislike,
        back_populates="disliked_by",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
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



class Tag(SQLModel, table=True):
    __tablename__ = "tags"

    id: int = Field(primary_key=True)
    name: str = Field(nullable=False, unique=True)
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    posts: List["Post"] = Relationship(
        link_model=PostTag,
        back_populates="tags",
        sa_relationship_kwargs={"lazy":"selectin"}
    )

    def __repr__(self) -> str:
        return f"<Tag {self.name}"



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
    comments: List["Comment"] = Relationship(back_populates="post", sa_relationship_kwargs={"lazy": "selectin"})
    tags: List[Tag] = Relationship(
        link_model=PostTag,
        back_populates="posts",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    liked_by: List["User"] = Relationship(
        link_model=Like,
        back_populates="likes",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    disliked_by: List["User"] = Relationship(
        link_model=Dislike,
        back_populates="dislikes",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))


class Comment(SQLModel, table=True):
    __tablename__ = "comments"

    id: int = Field(primary_key=True)
    content: str = Field(nullable=False)
    reactions: int = Field(default=0, nullable=False)
    author: User = Relationship(back_populates="comments")
    author_id: int = Field(default=None, foreign_key="users.id")
    post: Post = Relationship(back_populates="comments")
    post_id: int = Field(default=None, foreign_key="posts.id")



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
