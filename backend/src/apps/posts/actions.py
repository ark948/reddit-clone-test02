from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlmodel import select
from sqlalchemy import and_, or_
from sqlalchemy.orm import joinedload
from icecream import ic
ic.configureOutput(includeContext=True)
from pydantic import BaseModel
from typing import List
from src.apps.utils import myprint


from src.apps.tags.main import (
    GetPostsWithTags, TagsList
    )
from src.sections.database.models import User, Post, Like, Tag, PostTag
from src.apps.posts import crud



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



async def user_remove_like_from_post(post_id: int, user: User, session: AsyncSession) -> dict:
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
    


async def user_dislike_post(post_id: int, user: User, session: AsyncSession) -> dict[str, str]:
    postObj = await crud.get_post(post_id, session)

    if postObj is not None:
        if postObj in user.dislikes:
            return {"message": "Already disliked."}
        user.dislikes.append(postObj)
        postObj.reactions -= 1
    else:
        return {"message": "Post not found - 404"}
        
    try:
        await session.commit()
        return {"message": "success"}
    except Exception as error:
        print("ERROR IN COMMIT", error)
        return {"message": "Error occurred."}
    


async def user_remove_dislike_from_post(post_id: int, user: User, session: AsyncSession) -> dict[str, str]:
    postObj = await crud.get_post(post_id, session)
    if postObj is None:
        return {"message": "Post not found - 404"}
    
    if postObj in user.dislikes:
        user.dislikes.remove(postObj)
        postObj.reactions += 1
    else:
        return {"message": "User has not disliked this post."}
    
    try:
        await session.commit()
        return {"message": "success"}
    except Exception as error:
        print("ERROR IN COMMIT", error)
        return {"message": "Error occurred"}
    
    

async def select_posts_with_tags(list_of_tags: GetPostsWithTags, session: AsyncSession):
    # THIS WORKS USING THE Association table
    # Need to figure it out a way to get items using join
    # selected_tag_objs = []
    # selected_posts = []
    # for item in list_of_tags.tags:
    #     stmt = select(Tag).where(Tag.name==item.name)
    #     result = await session.scalar(stmt)
    #     selected_tag_objs.append(result)

    # for tag in selected_tag_objs:
    #     # stmt = select(Post).where(Tag.id==tag.id) THIS ALSO WORKS but raises a warning
    #     stmt = select(Post).select_
    #     result = await session.scalar(stmt)
    #     selected_posts.append(result)

    selected_tag_objs = []
    selected_posts_ids = []
    for item in list_of_tags.tags:
        stmt = select(Tag).where(Tag.name==item.name)
        result = await session.scalar(stmt)
        selected_tag_objs.append(result)
    
    for tag_item in selected_tag_objs:
        stmt = select(PostTag).where(PostTag.tag_id==tag_item.id)
        result = await session.scalars(stmt)
        for i in result.all():
            selected_posts_ids.append(i.post_id)
    
    actual_post_items = []
    for post_id in selected_posts_ids:
        result = await session.get(Post, post_id)
        actual_post_items.append(result)
    return actual_post_items




async def select_posts_with_tags_v2(list_of_tags: TagsList, session: AsyncSession):
    
    result = await session.scalars(
            select(Tag.id)
            .where(Tag.name.in_([*list_of_tags.names]))
        )
    tag_ids = result.all()

    result = await session.scalars(
        select(Post)
        .where(Post.id.in_(
            select(PostTag.post_id)
            .where(PostTag.tag_id.in_([*tag_ids]))
        ))
    )
    post_objs = result.all()
    return post_objs
    
    
