import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio.session import AsyncSession



from src.sections.database.models import Community



@pytest.mark.asyncio
async def test_app_comments_test_route(async_client: AsyncClient, load_data):
    resposne = await async_client.get('/apps/comments/test')

    assert resposne.status_code == 200
    assert resposne.json() == "ok"


@pytest.mark.asyncio
async def test_app_comments_add(async_client: AsyncClient, load_data):
    # user 2 will comment on the first post (only post) of user 1
    post_id = load_data["user1"].posts[0].id
    resposne = await async_client.post(
        url=f"/apps/comments/add/{post_id}",
        json={
            "content": "Nice post"
        },
        headers={
            "Authorization": f"Bearer {load_data['user2Token']}"
        }
    )

    assert resposne.status_code == 201



@pytest.mark.asyncio
async def test_app_comments_get(async_client: AsyncClient, load_data):
    # user 2 will comment on the first post (only post) of user 1
    post_id = load_data["user1"].posts[0].id
    resposne = await async_client.post(url=f"/apps/comments/add/{post_id}", json={ "content": "Nice post" },
        headers={
            "Authorization": f"Bearer {load_data['user2Token']}"
        }
    )

    assert resposne.status_code == 201

    resposne = await async_client.get('/apps/comments/get/1')

    assert resposne.status_code == 200
    assert resposne.json()["content"] == "Nice post"
    assert resposne.json()["author_id"] == load_data["user2"].id
    assert resposne.json()["post_id"] == post_id