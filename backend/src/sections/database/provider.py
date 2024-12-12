from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from sqlmodel import create_engine
from sqlmodel import SQLModel
from typing import AsyncGenerator


# local imports
from src.configs.settings import Config


async_engine = AsyncEngine(
    create_engine(url=Config.DB_URL)
)


async def init_db():
    async with async_engine.begin() as conn:
        from src.sections.database.models import User

        await conn.run_sync(SQLModel.metadata.create_all)
        statement = text("SELECT 'database connected';")
        result = await conn.execute(statement)
        print(result.all())
