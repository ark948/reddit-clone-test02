import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio.session import AsyncSession
from icecream import ic
ic.configureOutput(includeContext=True)



from src.sections.database.models import Post



@pytest.mark.asyncio
async def test_app_posts_test_route(async_client: AsyncClient):
    response = await async_client.get('/apps/posts/test')

    assert response.status_code == 200
    assert response.json()["message"] == "posts app ok"



@pytest.mark.asyncio
async def test_app_posts_routes_get_post(async_client: AsyncClient, load_users_with_posts):
    response = await async_client.get('/apps/posts/get-post/1')

    assert response.status_code == 200

    data = response.json()
    post = load_users_with_posts[0].posts[0]
    assert data["id"] == post.id
    assert data["title"] == post.title
    assert data["owner_id"] == post.owner_id