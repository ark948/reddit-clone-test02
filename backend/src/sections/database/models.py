import uuid
from datetime import datetime
from sqlalchemy.dialects import postgresql as pg
from typing import (
    Optional
)
from sqlmodel import (
    SQLModel, Field, Column, Relationship
)





class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int = Field(primary_key=True)
    uid: uuid.UUID = Field(sa_column=Column(pg.UUID, nullable=False, default=uuid.uuid4))
    username: str = Field(unique=True, nullable=False)
    email: str = Field(unique=True, nullable=False)
    role: str = Field(sa_column=Column(pg.VARCHAR, nullable=False, server_default="user"))
    is_verified: bool = Field(default=False)
    password_hash: str = Field(exclude=True)  # exclude -> do not serialize
    profile_id: Optional[int] = Field(default=None, foreign_key="profiles.id")
    profile: Optional["Profile"] = Relationship(back_populates="user")
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

    def __repr__(self):
        return f'<User {self.username}>'
    
    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    

class Profile(SQLModel, table=True):
    __tablename__ = "profiles"
    
    id: int = Field(primary_key=True)
    first_name: str = Field(nullable=True)
    last_name: str = Field(nullable=True)
    karma: int = Field(default=0)
    # user_id: Optional[int] = Field(default=None, foreign_key="users.id") # new (we'll go for now, untill sure) update: This does not work
    user: Optional["User"] = Relationship(
        sa_relationship_kwargs={"uselist": False},
        back_populates="profile"
    )