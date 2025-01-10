from sqlalchemy.ext.asyncio.session import AsyncSession
from typing import Union


# local imports
from backend.sections.database.models import User, Post, Like



async def get_post(post_id: int, session: AsyncSession) -> Union[Post, None]:
    try:
        postObj = await session.get(Post, post_id)
    except Exception as error:
        print("ERROR IN post CRUD>GET", error)
        return None
    return postObj
    