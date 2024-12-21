from sqlmodel import select
from dataclasses import dataclass
from sqlalchemy.ext.asyncio.session import AsyncSession
from fastapi import Depends


from src.sections.database.connection import get_async_session
from src.sections.database.models import Community


@dataclass
class CommunityService:
    session: AsyncSession = Depends(get_async_session)


    async def get_community(self, item_id: int) -> Community | None:
        try:
            obj = await self.session.scalar(select(Community).where(Community.id == item_id))
            return obj
        except Exception as error:
            print("ERROR IN GETTING ITEM: ", error)
            return None