from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from sqlmodel import create_engine
from sqlmodel import SQLModel


# local imports
from src.configs import Config


async_engine = AsyncEngine(
    create_engine(url=Config.DB_URL)
)


async def init_db():
    async with async_engine.begin() as conn:
        # import models

        await conn.run_sync(SQLModel.metadata.create_all)
        statement = text("SELECT 'hello';")
        result = await conn.execute(statement)
        print(result.all())


async def get_async_session() -> AsyncSession:
    Session = sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with Session() as session:
        yield session
