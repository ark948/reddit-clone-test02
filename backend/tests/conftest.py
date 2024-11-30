import pytest
import asyncio
from httpx import AsyncClient
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator
from httpx import ASGITransport, AsyncClient


# local imports
from src import app
from src.sections.database.dependencies import get_async_session
from src.sections.database.models import User
from src.sections.authentication.hash import genereate_password_hash
from src.configs.settings import Config


# drop all database every time when test complete
@pytest.fixture(scope='session')
async def async_db_engine():

    async_engine = create_async_engine(
        url=Config.DB_URL,
        echo=True
    )
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield async_engine

    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


# truncate all table to isolate tests
@pytest.fixture(scope='function')
async def async_db(async_db_engine):
    async_session = sessionmaker(
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
        bind=async_db_engine,
        class_=AsyncSession,
    )

    async with async_session() as session:
        await session.begin()
        yield session
        await session.rollback()
        for table in reversed(SQLModel.metadata.sorted_tables):
            await session.execute(f'TRUNCATE {table.name} CASCADE;')
            await session.commit()


@pytest.fixture(scope='function', name='ac')
async def async_client() -> AsyncGenerator[AsyncSession, None]:
    def override_get_db(async_db):
        try:
            yield async_db
        finally:
            async_db.close()

    app.dependency_overrides[get_async_session] = override_get_db
    client = AsyncClient(transport=ASGITransport(app=app), base_url="http://127.0.0.1:8000/")
    yield client

# let test session to know it is running inside event loop
@pytest.fixture(scope='session')
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()

# assume we have a example model
@pytest.fixture
async def async_example_orm(async_db: AsyncSession) -> User:
    example = User(username="tester01", email='tester01@email.com',
                   password_hash=genereate_password_hash('123'))
    async_db.add(example)
    await async_db.commit()
    await async_db.refresh(example)
    return example
