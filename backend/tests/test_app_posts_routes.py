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
async def test_app_posts_routes_get_post(async_client: AsyncClient, load_data):
    response = await async_client.get('/apps/posts/get-post/1')

    assert response.status_code == 200

    data = response.json()
    assert data["title"] == load_data["user1"].posts[0].title
    assert data["community_id"] == load_data["user1"].communities[0].id
    assert data["owner_id"] == load_data["user1"].id


@pytest.mark.asyncio
async def test_app_posts_routes_create_post(async_client: AsyncClient, load_data):
    response = await async_client.post(
        url=f"/apps/posts/create-post/1",
        json={
            "title": "Second post",
            "body": "and the body."
        },
        headers={
            "Authorization": f"Bearer {load_data['user1Token']}"
        }
    )

    assert response.status_code == 201

    data = response.json()
    assert data["title"] == "Second post"
    assert data["id"] == 2
    assert data["owner_id"] == load_data["user1"].id
    assert data["body"] == "and the body."
    assert data["community_id"] == 1
    assert data["reactions"] == 0


@pytest.mark.asyncio
async def test_app_posts_routes_edit_post(async_client: AsyncClient, load_data):
    user1 = load_data["user1"]
    resposne = await async_client.put(
        url="/apps/posts/edit-post/1",
        json={
            "title": "post 1 edited",
            "body": "body also edited."
        },
        headers={
            "Authorization": f"Bearer {load_data['user1Token']}"
        }
    )

    assert resposne.status_code == 200

    data = resposne.json()
    assert data["title"] == "post 1 edited"
    assert data["id"] == 1
    assert data["owner_id"] == user1.id
    assert data["body"] == "body also edited."
    assert data["community_id"] == 1
    assert data["reactions"] == 0


@pytest.mark.asyncio
async def test_app_posts_routes_delete_post(async_client: AsyncClient, async_db: AsyncSession, load_data):
    resposne = await async_client.delete(
        url="/apps/posts/delete-post/1",
        headers={
            "Authorization": f"Bearer {load_data['user1Token']}"
        }
    )

    assert resposne.status_code == 204
    
    resposne = await async_client.get(url="/apps/posts/get-post/1")
    assert resposne.status_code == 404

    post_item = await async_db.get(Post, 1)
    assert post_item == None

    
@pytest.mark.asyncio
async def test_app_posts_routes_get_user_posts(async_client: AsyncClient, async_db: AsyncSession, load_data):
    response = await async_client.get('/apps/posts/get-user-posts', headers={
        "Authorization": f"Bearer {load_data['user1Token']}"
    })

    assert response.status_code == 200

    data = response.json()
    assert len(data) == 1
    assert data[0]['id'] == load_data["user1"].posts[0].id


@pytest.mark.asyncio
async def test_app_posts_routes_user_liked_posts(async_client: AsyncClient, load_data):
    response = await async_client.post(
        url='/apps/posts/like-post/1',
        headers={
            "Authorization": f"Bearer {load_data['user2Token']}"
        }
    )

    assert response.status_code == 200
    assert len(load_data["user2"].likes) == 1
    assert load_data["user2"].likes[0].id == 1
    assert load_data["user2"].likes[0].owner_id == 1    


@pytest.mark.asyncio
async def test_app_posts_routes_user_like_post(async_client: AsyncClient, load_data):
    response = await async_client.post(
        url='/apps/posts/like-post/1',
        headers={
            "Authorization": f"Bearer {load_data['user2Token']}"
        }
    )

    assert response.status_code == 200

    data = response.json()
    assert data["status"] == True
    assert data["message"] == "success"
    assert len(load_data["user2"].likes) == 1
    assert load_data["user2"].likes[0].id == 1
    assert load_data["user2"].likes[0].owner_id == 1