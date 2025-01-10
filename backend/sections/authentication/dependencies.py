from fastapi import Depends, HTTPException
from typing import Annotated, Union
from sqlalchemy.ext.asyncio.session import AsyncSession
from redis.asyncio import Redis
from icecream import ic
ic.configureOutput(includeContext=True)


# local imports
from backend.sections.authentication.service import UserService
from backend.sections.database.models import User
from backend.sections.redis import get_redis
from backend.sections.redis import add_jti_to_blocklist, token_in_blocklist
from backend.sections.errors import InvalidToken
from backend.sections.database.connection import get_async_session
from backend.sections.authentication.crud import (
    get_user_by_email
)
from backend.sections.authentication.tokens import (
    TokenBearer,
    AccessTokenBearer
)



async def get_users_service(session: AsyncSession = Depends(get_async_session)) -> UserService:
    return UserService(session=session)



async def get_current_user(
        token_details: dict = Depends(AccessTokenBearer()),
        session: AsyncSession = Depends(get_async_session),
        redis_client: Redis = Depends(get_redis)
        ) -> Union[User, None]:
    try:
        response = await token_in_blocklist(token_details['jti'], redis_client)
    except Exception as error:
        ic("Error in getting jti from redis", error)
        raise HTTPException(status_code=500)
    if response:
        raise InvalidToken()
    else:
        user_email = token_details["user"]["email"]
        user = await get_user_by_email(user_email, session)
        return user
    


UserServiceDep = Annotated[UserService, Depends(get_users_service)]
token_req = Depends(TokenBearer())
getCurrentUserDep = Annotated[User, Depends(get_current_user)]