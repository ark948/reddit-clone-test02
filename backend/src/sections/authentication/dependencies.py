from fastapi import Depends
from typing import Annotated, Union
from sqlalchemy.ext.asyncio.session import AsyncSession


# local imports
from src.sections.authentication.service import UserService
from src.sections.database.models import User
from src.sections.database.connection import get_async_session
from src.sections.authentication.crud import (
    get_user_by_email
)
from src.sections.authentication.tokens import (
    TokenBearer,
    AccessTokenBearer
)



async def get_users_service(session: AsyncSession = Depends(get_async_session)) -> UserService:
    return UserService(session=session)



async def get_current_user(token_details: dict = Depends(AccessTokenBearer()), session: AsyncSession = Depends(get_async_session)) -> Union[User, None]:
    user_email = token_details["user"]["email"]
    user = await get_user_by_email(user_email, session)
    return user



UserServiceDep = Annotated[UserService, Depends(get_users_service)]
token_req = Depends(TokenBearer())
getCurrentUserDep = Annotated[User, Depends(get_current_user)]