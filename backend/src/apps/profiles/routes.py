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
from src.apps.profiles.schemas import ProfileModel, UpdateProfile
from src.sections.database.connection import get_async_session
from src.apps.profiles.schemas import ProfileFromUser
from src.sections.authentication.dependencies import getCurrentUserDep
from src.sections.database.dependencies import AsyncSessionDep


router = APIRouter(
    prefix='/profile',
    tags=['profile']
)


@router.get('/')
async def index():
    return "Profile Index"



# this works so far
@router.get('/get-profile', response_model=ProfileModel, status_code=status.HTTP_200_OK)
async def get_profile_from_user_id(user: getCurrentUserDep, session: AsyncSession=Depends(get_async_session)):
    stmt = await session.execute(
        select(User)
        .options(joinedload(User.profile))
        .where(User.id==user.id)
    )
    result = stmt.scalar()
    return result.profile



@router.get('/get-profile-v2', response_model=ProfileModel, status_code=status.HTTP_200_OK)
async def get_profile_from_user_id_v2(user: getCurrentUserDep, session: AsyncSession=Depends(get_async_session)):
    stmt = await session.execute(
        select(Profile)
        .where(Profile.id==user.profile_id)
    )
    profile = stmt.scalar()
    return profile


@router.put('/update-profile', response_model=ProfileModel, status_code=status.HTTP_200_OK)
async def update_profile(user: getCurrentUserDep, profile_update_data: UpdateProfile, session: AsyncSessionDep):
    response = await crud.update_profile(user.profile_id, profile_update_data, session)
    return response
    
