from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlmodel import select


from src.sections.database.models import Community
from src.sections.database.models import User
from src.apps.communities import crud


async def user_join_community(community_id: int, user: User, session: AsyncSession) -> int | None:
    try:
        community_obj = await crud.get_community(community_id, session)
    except Exception as error:
        print("Community does not exist", error)
        return None
    
    try:
        user.communities.append(community_obj)
    except Exception as error:
        print("Error in join user - community", error)
        return None

    try:
        await session.commit()
    except Exception as error:
        print("ERROR IN SAVE", error)

    return 1

async def user_leave_community(community_id: int, user: User, session: AsyncSession) -> int | None:
    try:
        community_obj = await crud.get_community(community_id, session)
    except Exception as error:
        print("Community does not exist", error)
        return None
    
    try:
        user.communities.remove(community_obj)
    except ValueError as error:
        print("Value does not exist.", error)
        return None

    try:
        await session.commit()
    except Exception as error:
        print("ERROR IN SAVE", error)
        return None

    return 1