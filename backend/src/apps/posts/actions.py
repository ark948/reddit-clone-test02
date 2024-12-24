from sqlalchemy.ext.asyncio.session import AsyncSession


from src.sections.database.models import User, Post


async def user_like_post(post_id: int, user: User, session: AsyncSession) -> dict | bool:
    try:
        postObj = await session.get(Post, post_id)
    except Exception as error:
        print("Post Not Found - 404", error)
        return False
    
    try:
        if postObj in user.likes:
            return {
                "status": False,
                "message": "ERROR, You have already liked this post."
            }
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
    return {
        "status": True,
        "message": "success"
    }
