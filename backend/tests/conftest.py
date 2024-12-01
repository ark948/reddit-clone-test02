import pytest
import asyncio
import pytest_anyio
from httpx import AsyncClient
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncConnection, async_scoped_session, async_sessionmaker
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator, AsyncIterator
from httpx import ASGITransport, AsyncClient
from sqlalchemy.pool import NullPool
from contextlib import asynccontextmanager
import pytest_asyncio


# local imports
from src import app
from src.sections.database.dependencies import get_async_session
from src.sections.database.models import User
from src.sections.authentication.hash import genereate_password_hash
from src.configs.settings import Config


async_engine = create_async_engine(
    url=Config.DB_URL,
    echo=False,
    poolclass=NullPool
)


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


@pytest_asyncio.fixture(scope="function", autouse=True)
async def async_client(async_db):
    def override_get_db():
        yield async_db
    app.dependency_overrides[get_async_session] = override_get_db
    return AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost")


# pytest-asyncio provides event loop