from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlmodel import select
from typing import Union
from icecream import ic
ic.configureOutput(includeContext=True)



# local imports
from src.sections.database.connection import get_async_session
from src.apps.communities.schemas import CreateCommunity
from src.sections.database.models import Community



async def get_community(item_id: int, session: AsyncSession) -> Union[Community, None]:
    stmt = select(Community).where(Community.id == item_id)
    try:
        item = await session.scalar(stmt)
    except Exception as error:
        print("ERROR IN CRUD get")
        print(error)
        return None
    return item


async def create_community(data: CreateCommunity, session: AsyncSession) -> Union[Community, None]:
    try:
        data_dict = data.model_dump()
        community_oject = Community(**data_dict)
    except Exception as error:
        print("ERROR IN CRUD CreateCommunity")
        print(error)
        return None
    try:
        session.add(community_oject)
    except Exception as error:
        print("ERROR IN CRUD add")
        print(error)
        return None
    try:
        await session.commit()
        await session.refresh(community_oject)
    except Exception as error:
        print("ERROR IN CRUD commit")
        print(error)
        return None
    return community_oject

async def get_all(session: AsyncSession):
    try:
        obj_list = await session.scalars(select(Community))
    except Exception as error:
        print("ERROR IN GETTING LIST", error)

    return obj_list.all()