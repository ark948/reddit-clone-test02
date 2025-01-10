from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlmodel import select
from sqlmodel import select
from dataclasses import dataclass
from sqlalchemy.ext.asyncio.session import AsyncSession
from fastapi import Depends


from backend.sections.database.connection import get_async_session
from backend.sections.database.models import Community
from backend.sections.database.models import Community
from backend.sections.database.models import User
from backend.apps.communities import crud
from backend.apps.utils import myprint




async def search_community_by_title(title: str, session: AsyncSession):

    results = await session.scalars(
        select(Community)
        .where(Community.title.icontains(f"%{title}%"))
    )

    return results.all()