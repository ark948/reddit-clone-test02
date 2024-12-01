import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.sections.database.models import User
from src.sections.authentication.hash import genereate_password_hash


@pytest.mark.asyncio
async def test_main_test_route(async_client: AsyncClient):
    resp = await async_client.get('/test')

    assert resp.status_code == 200
    assert resp.json()['message'] == "test successful"



@pytest.mark.asyncio
async def test_auth_test_route(async_client: AsyncClient):
    resp = await async_client.get('/auth/test')

    assert resp.status_code == 200
    assert resp.json() == {'message': "auth test route successful"}



@pytest.mark.asyncio
async def test_create_and_get_user(async_db: AsyncSession, async_client: AsyncClient):
    new_user = User(username="tester01", email="tester01@email.com", password_hash=genereate_password_hash('123'))
    async_db.add(new_user)
    await async_db.commit()

    resp = await async_client.get('auth/get-user-v3/1')
    data = resp.json()

    assert resp.status_code == 200
    assert data['username'] == "tester01"
    assert data['email'] == "tester01@email.com"