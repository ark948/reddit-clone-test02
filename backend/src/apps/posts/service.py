from sqlmodel import select
from dataclasses import dataclass
from sqlalchemy.ext.asyncio.session import AsyncSession
from fastapi import Depends


from src.sections.database.connection import get_async_session
from src.sections.database.models import User, Post
from src.apps.posts.schemas import CreatePost



@dataclass
class PostService:
    session: AsyncSession = Depends(get_async_session)

    async def get_post(self, item_id: int) -> Post | None:
        try:
            post_obj = await self.session.scalar(
                select(Post).where(Post.id == item_id)
            )
        except Exception as error:
            print("ERROR IN GETTING post ITEM: ", error)
            return None
        return post_obj
            

    async def create_post(self, user_id: int, post_data: CreatePost, community_id: int) -> Post | None:
        post_obj = Post(**post_data.model_dump())
        post_obj.owner_id = user_id
        post_obj.community_id = community_id
        if isinstance(post_obj, Post) == False: raise TypeError("ERROR IN CREATING post MODEL")
        try:
            self.session.add(post_obj)
            await self.session.commit()
        except Exception as error:
            print("ERROR IN COMMITTING post MODEL", error)
            return None
        return post_obj
    
