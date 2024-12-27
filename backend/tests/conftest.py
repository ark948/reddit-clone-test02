from httpx import AsyncClient
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from sqlalchemy.ext.asyncio import (
    create_async_engine, 
    AsyncConnection, 
    async_scoped_session, 
    async_sessionmaker
    )
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker, joinedload
from typing import AsyncGenerator, AsyncIterator
from httpx import ASGITransport, AsyncClient
from sqlalchemy.pool import NullPool
from contextlib import asynccontextmanager
from sqlalchemy import select
import pytest_asyncio
from redis import asyncio as redis
import fakeredis
from unittest import mock
from unittest.mock import MagicMock



# local imports
from src import app
from src.sections.redis import get_redis
from src.sections import redis
from src.sections.authentication.utils import create_access_token
from src.sections.database.dependencies import get_async_session
from src.sections.authentication.hash import generate_password_hash
from src.configs.settings import Config
from src.sections.database.models import (
    User,
    Community,
    Profile,
    Post
)


# this engine may not support exec method from sqlmodel session
async_engine = create_async_engine(url=Config.TEST_DB_URL, echo=False, poolclass=NullPool)


@pytest_asyncio.fixture(scope="function")
async def async_db_engine():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield async_engine
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def async_db(async_db_engine):
    async_session = async_sessionmaker(
        expire_on_commit=False, autocommit=False, autoflush=False, bind=async_db_engine, class_=AsyncSession
    )
    async with async_session() as session:
        await session.begin()
        yield session
        await session.rollback()


@pytest_asyncio.fixture
async def redis_client() -> AsyncIterator[redis.Redis]:
    async with fakeredis.FakeAsyncRedis() as client:
        yield client


# override_get_db was made async
@pytest_asyncio.fixture(scope="function", autouse=True)
async def async_client(async_db, redis_client):
    def override_get_db():
        yield async_db

    async def get_redis_override() -> redis.Redis:
        return redis_client

    app.dependency_overrides[get_async_session] = override_get_db
    app.dependency_overrides[get_redis] = get_redis_override
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost") as client:
        yield client


@pytest_asyncio.fixture(scope="function")
async def sample_user(async_db: AsyncSession):
    user_obj = User(username="test01", email="test01@email.com", password_hash=generate_password_hash('test123'))
    user_obj.role = "user"
    async_db.add(user_obj)
    await async_db.commit()
    return user_obj


@pytest_asyncio.fixture(scope="function")
async def login_data(sample_user):
    user_data = {
        "email": sample_user.email,
        "user_uid": str(sample_user.uid)
    }
    token = create_access_token(user_data)
    return token


@pytest_asyncio.fixture(scope="function")
async def multiple_users(async_db: AsyncSession):
    user_obj1 = User(username="test01", email="test01@email.com", password_hash=generate_password_hash('test123'))
    user_obj2 = User(username="test02", email="test02@email.com", password_hash=generate_password_hash('test123'))
    user_obj3 = User(username="test03", email="test03@email.com", password_hash=generate_password_hash('test123'))
    async_db.add(user_obj1)
    async_db.add(user_obj2)
    async_db.add(user_obj3)
    await async_db.commit()
    return [user_obj1, user_obj2, user_obj3]


@pytest_asyncio.fixture(scope="function")
async def sample_profile(async_db: AsyncSession, sample_user):
    profile_obj = Profile(first_name="Mike", last_name="Cobalt", karma=0, user=sample_user)
    async_db.add(profile_obj)
    await async_db.commit()
    return profile_obj


@pytest_asyncio.fixture(scope="function")
async def sample_community(async_db: AsyncSession):
    community_obj = Community(title="tech_fans", about="Cool facts about technology.")
    async_db.add(community_obj)
    await async_db.commit()
    return community_obj


@pytest_asyncio.fixture(scope="function")
async def multiple_communities(async_db: AsyncSession):
    community_obj01 = Community(title="co 1", about="about co 1")
    community_obj02 = Community(title="co 2", about="about co 2")
    community_obj03 = Community(title="co 3", about="about co 3")
    async_db.add_all([community_obj01, community_obj02, community_obj03])
    await async_db.commit()
    return [community_obj01, community_obj02, community_obj03]


@pytest_asyncio.fixture(scope="function")
async def sample_post(async_db: AsyncSession, sample_user, sample_community):
    postObj = Post(title="First Post for testing", body="And this is body.", owner_id=sample_user.id, community_id=sample_community.id)
    async_db.add(postObj)
    await async_db.commit()
    return postObj


@pytest_asyncio.fixture(scope="function")
async def load_users_with_posts(async_db: AsyncSession):
    # user
    # community
    # post
    pre_user = User(username="test01", email="test01@email.com", password_hash=generate_password_hash('test123'))
    pre_user2 = User(username="test02", email="test02@email.com", password_hash=generate_password_hash('test123'))
    pre_community = Community(title="tech_fans", about="Cool facts about technology.")
    
    async_db.add_all([pre_user, pre_user2])
    async_db.add(pre_community)
    await async_db.commit()

    pre_post = Post(title="First post", body="This is body.", owner_id=pre_user.id, community_id=pre_community.id)
    async_db.add(pre_post)
    await async_db.commit()

    user1 = await async_db.scalar(
        select(User)
        .options(joinedload(User.posts))
    )
    

    user2 = await async_db.scalar(
        select(User)
        .options(joinedload(User.posts))
    )
    
    return [user1, user2]

# pytest-asyncio provides event loop