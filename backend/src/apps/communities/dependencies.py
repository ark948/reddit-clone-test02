from sqlalchemy.ext.asyncio.session import AsyncSession
from fastapi import Depends


from src.apps.communities.service import CommunityService
from src.sections.database.dependencies import get_async_session


async def get_community_service_dep(session: AsyncSession = Depends(get_async_session)) -> CommunityService:
    return CommunityService(session=session)