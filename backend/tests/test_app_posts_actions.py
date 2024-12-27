import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio.session import AsyncSession
from icecream import ic
ic.configureOutput(includeContext=True)



from src.sections.database.models import Post
from src.apps.posts.actions import (
    user_like_post,
    user_remove_like_from_post,
    user_dislike_post,
    user_remove_dislike_from_post
)




@pytest.mark.asyncio
async def test_posts_app_actions_user_like(async_db: AsyncSession, load_users_with_posts):
    
    # ic(load_users_with_posts[0].posts)
    assert load_users_with_posts[0].posts[0].reactions == 0
    # user with id 2 will dislike post with id 1 that belong to user with id 1
    response = await user_like_post(1, load_users_with_posts[1], async_db)
    
    assert response["status"] == True
    assert response["message"] == "success"
    # ic(load_users_with_posts[0].posts)

    assert load_users_with_posts[0].posts[0].reactions == 1


@pytest.mark.asyncio
async def test_posts_app_actions_remove_like(async_db: AsyncSession, load_users_with_posts):
    response = await user_like_post(1, load_users_with_posts[1], async_db)
    assert response['status'] == True
    assert load_users_with_posts[0].posts[0].reactions == 1

    response = await user_remove_like_from_post(1, load_users_with_posts[1], async_db)
    assert response['message'] == "success"
    assert load_users_with_posts[0].posts[0].reactions == 0

    
@pytest.mark.asyncio
async def test_posts_app_actions_dislike_post(async_db: AsyncSession, load_users_with_posts):
    assert load_users_with_posts[0].posts[0].reactions == 0

    response = await user_dislike_post(1, load_users_with_posts[1], async_db)
    assert response["message"] == "success"
    assert load_users_with_posts[0].posts[0].reactions == -1


@pytest.mark.asyncio
async def test_posts_app_actions_remove_dislike_post(async_db: AsyncSession, load_users_with_posts):
    assert load_users_with_posts[0].posts[0].reactions == 0

    response = await user_dislike_post(1, load_users_with_posts[1], async_db)
    assert response["message"] == "success"
    assert load_users_with_posts[0].posts[0].reactions == -1

    resposne = await user_remove_dislike_from_post(1, load_users_with_posts[1], async_db)
    assert response["message"] == "success"
    assert load_users_with_posts[0].posts[0].reactions == 0