from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlmodel import select
from sqlalchemy import and_, or_
from sqlalchemy.orm import joinedload
from icecream import ic
ic.configureOutput(includeContext=True)
from pydantic import BaseModel
from typing import List
from backend.apps.utils import myprint


from backend.apps.tags.main import (
    GetPostsWithTags, 
    TagsList
    )
from backend.sections.database.models import User, Post, Like, Tag, PostTag
from backend.apps.posts import crud






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
    
    