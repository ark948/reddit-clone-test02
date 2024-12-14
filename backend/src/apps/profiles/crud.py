from sqlalchemy.ext.asyncio.session import AsyncSession

# local imports
from src.sections.database.connection import get_async_session
from src.sections.database.models import Profile
from src.apps.profiles.schemas import UpdateProfile


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
    

async def update_profile(current_profile: Profile, profile_data: UpdateProfile, session: AsyncSession):
    try:
        for k, v in profile_data.model_dump().items():
            setattr(current_profile, k, v)
        await session.commit()
    except Exception as error:
        print("\nERROR in updating profile\n", error)
        return None
    return current_profile
    