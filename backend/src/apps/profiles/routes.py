from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import joinedload
from typing import Dict, Union
from sqlmodel import select
from fastapi import (
    APIRouter,
    Depends,
    status
)

from icecream import ic
ic.configureOutput(includeContext=True)


# local imports
from src.apps.profiles import crud
from src.sections.database.models import Profile, User
from src.sections.authentication.schemas import UserModel
from src.apps.profiles.schemas import ProfileModel
from src.sections.database.connection import get_async_session
from src.apps.profiles.schemas import ProfileFromUser


router = APIRouter(
    prefix='/profile',
    tags=['profile']
)


@router.get('/')
async def index():
    return "Profile Index"



@router.get('/get-profile', response_model=ProfileModel, status_code=status.HTTP_200_OK)
async def get_profile_from_user_id(user_id: int, session: AsyncSession=Depends(get_async_session)):
    stmt = await session.execute(
        select(User)
        .options(joinedload(User.profile))
        .where(User.id==user_id)
    )
    result = stmt.scalar()
    return result.profile