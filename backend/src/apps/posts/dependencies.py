from typing import Annotated
from sqlalchemy.ext.asyncio.session import AsyncSession
from fastapi import Depends



from src.sections.database.dependencies import get_async_session
from src.apps.posts.service import PostService



async def get_post_service(session: AsyncSession = Depends(get_async_session)) -> PostService:
    return PostService(session=session)


postServiceDep = Annotated[PostService, Depends(get_post_service)]