import pytest_asyncio
import pytest
from sqlalchemy.ext.asyncio.session import AsyncSession
from httpx import AsyncClient
from unittest import mock

from icecream import ic



@pytest.mark.asyncio
async def test_user_profile(async_client: AsyncClient, sample_user):
    data = {
        "email": "test01@email.com",
        "password": "test123"
    }

    resp = await async_client.post('auth/login', json=data)
    assert resp.status_code == 200

    login_data = resp.json()
    ic(login_data)

    resp = await async_client.get('auth/me', headers={
        "Authorization": f"Bearer {login_data['access_token']}"
    })

    assert resp.status_code == 200
    data = resp.json()

    assert data["email"] == sample_user.email
    assert data["username"] == sample_user.username
    assert data["uid"] == str(sample_user.uid)

    resp = await async_client.get('auth/logout-v3', headers={
        "Authorization": f"Bearer {login_data['access_token']}"
    })

    assert resp.status_code == 200
    data = resp.json()
    assert data == {"message": "Logout OK"}

    resp = await async_client.get('auth/me', headers={
        "Authorization": f"Bearer {login_data['access_token']}"
    })

    assert resp.status_code == 401
    data = resp.json()
    assert data["message"] == "Token is invalid Or expired"
    assert data["resolution"] == "Please get new token"
    assert data["error_code"] == "invalid_token"
