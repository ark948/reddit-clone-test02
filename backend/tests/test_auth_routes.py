import json
import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio.session import AsyncSession
from fastapi.encoders import jsonable_encoder
from sqlmodel import (
    select
)


from src.sections.database.models import User
from src.sections.authentication.hash import genereate_password_hash, verify_password
from icecream import ic
ic.configureOutput(includeContext=True)

@pytest.mark.asyncio
async def test_auth_test_route(async_client: AsyncClient):
    resp = await async_client.get('auth/test')

    assert resp.status_code == 200
    assert resp.json()['message'] == "auth test route successful"


@pytest.mark.skip
@pytest.mark.asyncio
async def test_auth_get_all_users(async_client: AsyncClient):
    pass


@pytest.mark.asyncio
async def test_auth_get_all_users_v2_with_no_data(async_client: AsyncClient):
    resp = await async_client.get('auth/get-all-users-v2')

    assert resp.status_code == 200
    assert resp.json() == []



@pytest.mark.asyncio
async def test_auth_get_all_users_v2_with_data(async_db: AsyncSession, async_client: AsyncClient):
    new_user = User(username="tester01", email="tester01@email.com", password_hash=genereate_password_hash('123'))
    async_db.add(new_user)
    await async_db.commit()

    resp = await async_client.get('auth/get-all-users-v2')

    assert resp.status_code == 200
    assert resp.json()[0]['username'] == new_user.username
    assert resp.json()[0]['email'] == new_user.email



@pytest.mark.asyncio
async def test_auth_get_user_object(async_db: AsyncSession, async_client: AsyncClient):
    new_user = User(username="tester01", email="tester01@email.com", password_hash=genereate_password_hash('123'))
    async_db.add(new_user)
    await async_db.commit()

    resp = await async_client.get(f'auth/get-user/{new_user.id}')

    assert resp.status_code == 200
    assert resp.json()['username'] == new_user.username
    assert resp.json()['email'] == new_user.email



@pytest.mark.asyncio
async def test_auth_get_user_object_no_data(async_db: AsyncSession, async_client: AsyncClient):
    non_existent_user_id = 10
    resp = await async_client.get(f'auth/get-user/{non_existent_user_id}')

    assert resp.status_code == 200
    assert resp.json() == None



@pytest.mark.asyncio
async def test_auth_get_user_object_v2(async_db: AsyncSession, async_client: AsyncClient):
    new_user = User(username="tester01", email="tester01@email.com", password_hash=genereate_password_hash('123'))
    async_db.add(new_user)
    await async_db.commit()

    resp = await async_client.get(f'auth/get-user-v2/{new_user.id}')

    assert resp.status_code == 200
    assert resp.json()['username'] == new_user.username
    assert resp.json()['email'] == new_user.email


@pytest.mark.asyncio
async def test_auth_get_user_object_v2_no_data(async_db: AsyncSession, async_client: AsyncClient):
    non_existent_user_id = 10
    resp = await async_client.get(f'auth/get-user-v2/{non_existent_user_id}')

    assert resp.status_code == 200
    assert resp.json() == None


@pytest.mark.asyncio
async def test_auth_get_user_object_v3(async_db: AsyncSession, async_client: AsyncClient):
    new_user = User(username="tester01", email="tester01@email.com", password_hash=genereate_password_hash('123'))
    async_db.add(new_user)
    await async_db.commit()

    resp = await async_client.get(f'auth/get-user-v3/{new_user.id}')

    assert resp.status_code == 200
    assert resp.json()['username'] == new_user.username
    assert resp.json()['email'] == new_user.email


@pytest.mark.asyncio
async def test_auth_get_user_object_v3_no_data(async_db: AsyncSession, async_client: AsyncClient):
    non_existent_user_id = 10
    resp = await async_client.get(f'auth/get-user-v3/{non_existent_user_id}')

    assert resp.status_code == 200
    assert resp.json() == None


@pytest.mark.asyncio
async def test_auth_get_user_object_v4(async_db: AsyncSession, async_client: AsyncClient):
    new_user = User(username="tester01", email="tester01@email.com", password_hash=genereate_password_hash('123'))
    async_db.add(new_user)
    await async_db.commit()

    resp = await async_client.get(f'auth/get-user-v4/{new_user.id}')

    assert resp.status_code == 200
    assert resp.json()['username'] == new_user.username
    assert resp.json()['email'] == new_user.email


@pytest.mark.asyncio
async def test_auth_get_user_object_v4_no_data(async_db: AsyncSession, async_client: AsyncClient):
    non_existent_user_id = 10
    resp = await async_client.get(f'auth/get-user-v4/{non_existent_user_id}')

    assert resp.status_code == 200
    assert resp.json() == None



@pytest.mark.asyncio
async def test_auth_create_user_account(async_db: AsyncSession, async_client: AsyncClient):
    data = {
        "username": "some_user",
        "email": "someuser@test.com",
        "password": "test123"
    }

    resp = await async_client.post('auth/signup', json=data)
    assert resp.status_code == 201
    
    assert resp.json()['email'] == data['email']
    assert resp.json()['username'] == data['username']


@pytest.mark.asyncio
async def test_auth_create_user_account_v2(async_db: AsyncSession, async_client: AsyncClient):
    data = {
        "username": "some_user",
        "email": "someuser@test.com",
        "password": "test123"
    }

    resp = await async_client.post('auth/signup-v2', json=data)
    assert resp.status_code == 201
    
    assert resp.json()['email'] == data['email']
    assert resp.json()['username'] == data['username']


@pytest.mark.asyncio
async def test_auth_create_user_account_v3(async_db: AsyncSession, async_client: AsyncClient):
    data = {
        "username": "some_user",
        "email": "someuser@test.com",
        "password": "test123"
    }

    resp = await async_client.post('auth/signup-v3', json=data)
    assert resp.status_code == 201
    assert resp.json() == [1]