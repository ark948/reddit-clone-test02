from sqlmodel import select
from http import HTTPStatus
from sqlalchemy.ext.asyncio.session import AsyncSession
from datetime import datetime
from pydantic import BaseModel
from typing import List
from fastapi import (
    APIRouter,
    HTTPException
)
from icecream import ic
ic.configureOutput(includeContext=True)


from src.sections.database.dependencies import AsyncSessionDep
from src.sections.authentication.dependencies import getCurrentUserDep
from src.sections.database.models import Tag, Post



router = APIRouter(
    prefix="/tags",
    tags=["Tag"]
)




class TagSchema(BaseModel):
    id: int
    name: str
    created_at: datetime

class CreateTagSchema(BaseModel):
    name: str

class TagAddToPost(BaseModel):
    tags: List[CreateTagSchema]


class GetTags(BaseModel):
    # this was solely made to be used with GetPostsWithTags
    name: str


class GetPostsWithTags(BaseModel):
    tags: List[GetTags]



async def add_tags_to_post_action(post_item: Post, tags_list: TagAddToPost, session: AsyncSessionDep) -> Post:
    for tag_item in tags_list.tags:
        result = await session.exec(select(Tag).where(Tag.name==tag_item.name))
        tag = result.one_or_none()
        if not tag:
            tag = Tag(name=tag_item.name)
        
        post_item.tags.append(tag)
    session.add(post_item)
    await session.commit()
    await session.refresh(post_item)
    return post_item
        



@router.get('')
@router.get('/')
async def tags_root() -> str:
    return "tag ok"



@router.post('/add', response_model=TagSchema, status_code=HTTPStatus.CREATED)
async def add(data: CreateTagSchema, user: getCurrentUserDep, session: AsyncSessionDep) -> Tag:
    obj_dict = data.model_dump()
    obj = Tag(name=obj_dict["name"])
    try:
        session.add(obj)
        await session.commit()
        return obj
    except Exception as error:
        print("ERROR IN tag ADD: ", error)
        raise HTTPException(500)
    


@router.post('/add-tag/{post_id}', response_model=Post, status_code=HTTPStatus.OK)
async def add_tags_to_post(post_id: int, tags_to_add: TagAddToPost, user: getCurrentUserDep, session: AsyncSessionDep):
    for post in user.posts:
        if post_id == post.id:
            response = await add_tags_to_post_action(post, tags_to_add, session)
            return response
    else:
        raise HTTPException(404)