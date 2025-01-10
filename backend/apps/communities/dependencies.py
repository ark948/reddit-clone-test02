from sqlalchemy.ext.asyncio.session import AsyncSession
from fastapi import Depends


from backend.apps.communities.service import CommunityService
from backend.sections.database.dependencies import get_async_session


async def get_community_service_dep(session: AsyncSession = Depends(get_async_session)) -> CommunityService:
    return CommunityService(session=session)