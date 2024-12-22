import pytest
from sqlalchemy.ext.asyncio.session import AsyncSession
from httpx import AsyncClient



from src.sections.database.models import Profile
from src.apps.profiles.schemas import UpdateProfile



@pytest.mark.asyncio
async def test_profile_index(async_client: AsyncClient):
    response = await async_client.get('/apps/profile/')

    assert response.status_code == 200
    assert response.json() == "Profile Index"


@pytest.mark.asyncio
async def test_profile_get_profile(async_client: AsyncClient, sample_user, login_data, sample_profile):
    resposne = await async_client.get('/apps/profile/get-profile', headers={
        "Authorization": f"Bearer {login_data}"
    })

    assert resposne.status_code == 200

    data = resposne.json()
    assert data["id"] == 1
    assert data["first_name"] == sample_profile.first_name
    assert data["last_name"] == "Cobalt"


@pytest.mark.asyncio
async def test_profile_get_profile_v2(async_client: AsyncClient, sample_user, login_data, sample_profile):
    resposne = await async_client.get('/apps/profile/get-profile-v2', headers={
        "Authorization": f"Bearer {login_data}"
    })

    assert resposne.status_code == 200

    data = resposne.json()
    assert data["id"] == 1
    assert data["first_name"] == sample_profile.first_name
    assert data["last_name"] == "Cobalt"


@pytest.mark.asyncio
async def test_profile_update_profile(async_client: AsyncClient, sample_user, login_data, sample_profile):
    update_data = {
        "first_name": "John",
        "last_name": "Nolan"
    }
    response = await async_client.put('/apps/profile/update-profile', headers=
        {
            "Authorization": f"Bearer {login_data}"
        }, 
        json=update_data
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["first_name"] == sample_profile.first_name
    assert data["last_name"] == update_data["last_name"]