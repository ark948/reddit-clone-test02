import pytest_asyncio
import pytest
from sqlalchemy.ext.asyncio.session import AsyncSession
from httpx import AsyncClient
from unittest import mock



@pytest.mark.skip
@pytest.mark.asyncio
async def test_login(async_client: AsyncClient, sample_user):
    data = {
        "email": "test01@email.com",
        "password": "test123"
    }

    resp = await async_client.post('auth/login', json=data)
    assert resp.status_code == 200
    
    data = resp.json()
    assert data["message"] == "Login successful"
    assert data["user"]["email"] == sample_user.email
    assert data["user"]["uid"] == str(sample_user.uid)


@pytest.mark.skip
@pytest.mark.asyncio
async def test_user_profile(async_client: AsyncClient, sample_user):
    data = {
        "email": "test01@email.com",
        "password": "test123"
    }

    resp = await async_client.post('auth/login', json=data)
    assert resp.status_code == 200

    login_data = resp.json()

    resp = await async_client.get('auth/me-v4', headers={
        "Authorization": f"Bearer {login_data['access_token']}"
    })

    assert resp.status_code == 200
    data = resp.json()

    assert data["email"] == sample_user.email
    assert data["username"] == sample_user.username
    assert data["uid"] == str(sample_user.uid)



@pytest.mark.asyncio
async def test_logout(async_client: AsyncClient, sample_user):
    data = {
        "email": "test01@email.com",
        "password": "test123"
    }

    resp = await async_client.post('auth/login', json=data)
    assert resp.status_code == 200
    
    data = resp.json()
    assert data["message"] == "Login successful"
    assert data["user"]["email"] == sample_user.email
    assert data["user"]["uid"] == str(sample_user.uid)

    resp = await async_client.get('auth/logout-v2', headers={
        "Authorization": f"Bearer {data['access_token']}"
    })

    assert resp.status_code == 200
    data = resp.json()
    assert data["message"] == "Logged out successfully."