from datetime import datetime
from sqlmodel import select
from dataclasses import dataclass
from sqlalchemy.ext.asyncio.session import AsyncSession
from fastapi import Depends
from icecream import ic
ic.configureOutput(includeContext=True)


from src.sections.database.connection import get_async_session
from src.sections.database.models import User, Post
from src.apps.posts.schemas import (
    CreatePost,
    UpdatePost
)



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
            return post_obj
        except Exception as error:
            print("ERROR IN COMMITTING post MODEL", error)
            return None
        
    async def update_post(self, post_id: int, user_id: int, new_post_data: UpdatePost) -> Post | dict:
        try:
            postObj_to_update = await self.session.get(Post, post_id)
        except Exception as error:
            print("POST NOT FOUND, ", error)
            return None
        
        if postObj_to_update is not None:
            update_data_dict = new_post_data.model_dump()
            if update_data_dict["title"] == "" or update_data_dict["body"] == "":
                return {"message": "Both title and Body cannot be empty"}
            for k, v in update_data_dict.items():
                setattr(postObj_to_update, k, v)
            postObj_to_update.updated_at = datetime.now()
        else:
            return None
        
        try:
            await self.session.commit()
            return postObj_to_update
        except Exception as error:
            print("ERROR in commit update, ", error)
            return None
        
    async def delete_post(self, post_id: int, user_id: int) -> int | None:
        try:
            postObj_to_delete = await self.session.get(Post, post_id)
        except Exception as error:
            print("POST NOT FOUND, ", error)
            return None
        
        if postObj_to_delete is None:
            return None
        
        try:
            await self.session.delete(postObj_to_delete)
        except Exception as error:
            print("ERROR in DELETE: ", error)
            return None
        
        try:
            await self.session.commit()
            return 1
        except Exception as error:
            print("ERROR in DELETE commit: ", error)
            return None

        