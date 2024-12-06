from fastapi import Depends
from typing import Annotated
from sqlalchemy.ext.asyncio.session import AsyncSession


# local imports
from src.sections.authentication.service import UserService
from src.sections.database.dependencies import AsyncSessionDep
from src.sections.database.provider import get_async_session
from src.sections.authentication.tokens import TokenBearer



async def get_users_service(session: AsyncSession = Depends(get_async_session)) -> UserService:
    return UserService(session=session)



UserServiceDep = Annotated[UserService, Depends(get_users_service)]


token_req = Depends(TokenBearer())