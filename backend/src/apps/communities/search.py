from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlmodel import select
from sqlmodel import select
from dataclasses import dataclass
from sqlalchemy.ext.asyncio.session import AsyncSession
from fastapi import Depends


from src.sections.database.connection import get_async_session
from src.sections.database.models import Community
from src.sections.database.models import Community
from src.sections.database.models import User
from src.apps.communities import crud
from src.apps.utils import myprint




async def search_community_by_title(title: str, session: AsyncSession):

    results = await session.scalars(
        select(Community)
        .where(Community.title.icontains(f"%{title}%"))
    )

    return results.all()