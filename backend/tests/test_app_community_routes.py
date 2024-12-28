import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio.session import AsyncSession



from src.sections.database.models import Community




@pytest.mark.asyncio
async def test_app_community_test_route(async_client: AsyncClient):
    response = await async_client.get('/apps/community/test')

    assert response.status_code == 200
    assert response.json() == 'community test route'



@pytest.mark.asyncio
async def test_app_community_get_community(async_client: AsyncClient, sample_community):
    assert isinstance(sample_community, Community) == True
    assert sample_community.id == 1

    response = await async_client.get('/apps/community/get-community/1')

    assert response.status_code == 200

    data = response.json()
    assert data['id'] == 1
    assert data['title'] == sample_community.title
    assert data['about'] == sample_community.about
    assert data['users'] == []


@pytest.mark.asyncio
async def test_app_community_create_community(async_client: AsyncClient, async_db: AsyncSession):
    data = {
        "title": "Movie fans",
        "about": "A community for movie lovers."
    }

    response = await async_client.post('/apps/community/', json=data)
    assert response.status_code == 201

    data = response.json()
    assert data['id'] == 1
    assert data['title'] == "Movie fans"
    assert data["about"] == "A community for movie lovers."


@pytest.mark.asyncio
async def test_app_community_join(async_client: AsyncClient, redis_client, sample_user, sample_community):
    data = {
        "email": "test01@email.com",
        "password": "test123"
    }

    resp = await async_client.post('auth/login', json=data)
    assert resp.status_code == 200
    
    login_data = resp.json()

    response = await async_client.post('/apps/community/join/1', headers={
        "Authorization": f"Bearer {login_data['access_token']}"
    })

    assert response.status_code == 200
    assert response.json()['message'] == "Successfully joined."


@pytest.mark.asyncio
async def test_app_community_list_of_joined_communities(async_client: AsyncClient, async_db: AsyncSession, redis_client, sample_user, sample_community):
    data = {
        "email": "test01@email.com",
        "password": "test123"
    }

    resp = await async_client.post('auth/login', json=data)
    assert resp.status_code == 200
    
    login_data = resp.json()
    sample_user.communities.append(sample_community)
    await async_db.commit()
    resposne = await async_client.get('/apps/community/user-joined-list', headers={
        "Authorization": f"Bearer {login_data['access_token']}"
    })
    
    data = resposne.json()
    assert data[0]["title"] == "tech_fans"
    assert data[0]["about"] == "Cool facts about technology."