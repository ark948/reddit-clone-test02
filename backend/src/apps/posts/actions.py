from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlmodel import select
from sqlalchemy import and_
from sqlalchemy.orm import joinedload
from icecream import ic
ic.configureOutput(includeContext=True)


from src.sections.database.models import User, Post, Like


async def user_like_post(post_id: int, user: User, session: AsyncSession) -> dict | bool:
    try:
        postObj = await session.get(Post, post_id)
    except Exception as error:
        print("Post Not Found - 404", error)
        return False
    
    try:
        if postObj in user.likes:
            return { "status": False, "message": "ERROR, You have already liked this post." }
        user.likes.append(postObj)
        postObj.reactions += 1
    except Exception as error:
        print("ERROR IN like PROCESS 01", error)
        return False
    
    try:
        await session.commit()
    except Exception as error:
        print("ERROR IN like PROCESS 02", error)
        return False
    return { "status": True, "message": "success" }

async def user_remove_like_from_post(post_id: int, user: User, session: AsyncSession):
    try:
        postObj = await session.get(Post, post_id)
    except Exception as error:
        print("Post Not Found - 404", error)
        return {"message": "Post not found."}
    
    if postObj in user.likes:
        user.likes.remove(postObj)
        postObj.reactions -= 1
    else:
        print("USER HAS NOT LIKED THIS POST")
        return {"message": "User has not liked this post."}

    try:
        await session.commit()
        return {"message": "success"}
    except Exception as error:
        print("ERROR IN COMMIT", error)
        return {"message": "Error occurred."}