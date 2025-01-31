from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlmodel import select

# local imports
from backend.sections.database.connection import get_async_session
from backend.sections.database.models import Profile
from backend.apps.profiles.schemas import UpdateProfile


async def get_profile(item_id: int, sessino: AsyncSession):
    try:
        profile_obj = await sessino.scalar(
            select(Profile).where(Profile.id==item_id)
        )
    except Exception as error:
        print("ERROR IN GETTING profile ITEM: ", error)
        return None
    return profile_obj


async def create_profile(user_id: int, session: AsyncSession):
    try:
        new_profile_object = Profile(user_id=user_id)
    except Exception as error:
        print("\nError in creating profile\n", error)
        return None
    
    try:
        session.add(new_profile_object)
        await session.commit()
    except Exception as error:
        print("\nError in saving profile\n", error)
        return None
    
    return new_profile_object
    

async def update_profile(profile_id: int, profile_data: UpdateProfile, session: AsyncSession):
    profile = await session.scalar(select(Profile).where(Profile.id==profile_id))
    try:
        for k, v in profile_data.model_dump().items():
            setattr(profile, k, v)
        await session.commit()
    except Exception as error:
        print("\nERROR in updating profile\n", error)
        return None
    return profile
    