import uuid
from datetime import datetime
from sqlalchemy.dialects import postgresql as pg
from sqlmodel import (
    SQLModel, Field, Column 
)





class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int = Field(primary_key=True)
    uid: uuid.UUID = Field(sa_column=Column(pg.UUID, nullable=False, default=uuid.uuid4))
    username: str
    email: str
    first_name: str = Field(nullable=True)
    last_name: str = Field(nullable=True)
    role: str = Field(sa_column=Column(pg.VARCHAR, nullable=False, server_default="user"))
    is_verified: bool = Field(default=False)
    password_hash: str = Field(exclude=True)  # exclude -> do not serialize
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

    def __repr__(self):
        return f'<User {self.username}>'
    
    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    