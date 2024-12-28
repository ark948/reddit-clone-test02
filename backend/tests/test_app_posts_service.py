import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlmodel import select
from sqlalchemy.orm import joinedload
from icecream import ic




from src.apps.posts.service import PostService
from src.sections.database.models import Post, User
from src.apps.posts.schemas import CreatePost




@pytest.mark.asyncio
async def test_posts_app_service_get_post(async_db: AsyncSession, load_users_with_posts):
    postObj = await PostService(async_db).get_post(1)

    assert isinstance(postObj, Post) == True
    assert postObj == load_users_with_posts[0].posts[0]


@pytest.mark.asyncio
async def test_posts_app_service_create_post(async_db: AsyncSession, load_users_with_posts):

    pre_post = CreatePost(title="title1", body="body1")
    response = await PostService(async_db).create_post(1, pre_post, 1)

    assert isinstance(response, Post) == True
    
    search_query = await async_db.scalars(
        select(Post)
        .where(Post.owner_id==1)
    )
    all_user_posts = search_query.all()
    
    assert len(all_user_posts) == 2
    assert all_user_posts[1].title == "title1"
    assert all_user_posts[1].owner_id == load_users_with_posts[0].id