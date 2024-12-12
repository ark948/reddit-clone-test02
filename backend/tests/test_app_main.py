import json
import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlmodel import (
    select
)


from src.sections.database.models import User
from src.sections.authentication.hash import generate_password_hash, verify_password
from icecream import ic
ic.configureOutput(includeContext=True)

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
    new_user = User(username="tester01", email="tester01@email.com", password_hash=generate_password_hash('123'))
    async_db.add(new_user)
    await async_db.commit()

    resp = await async_client.get('auth/get-user-v3/1')
    data = resp.json()

    assert resp.status_code == 200
    assert data['username'] == "tester01"
    assert data['email'] == "tester01@email.com"


    second_user = User(username="tester02", email="tester02@email.com", password_hash=generate_password_hash('123'))
    async_db.add(second_user)
    await async_db.commit()

    resp = await async_client.get('auth/get-user-v3/2')
    data = resp.json()

    assert resp.status_code == 200
    assert data['username'] == "tester02"
    assert data['email'] == "tester02@email.com"


@pytest.mark.asyncio
async def test_get_user_from_session(async_db: AsyncSession):
    user = User(username="tester01", email="tester01@email.com", password_hash=generate_password_hash('123'))
    async_db.add(user)
    await async_db.commit()

    stmt = select(User).where(User.id==1)
    result = await async_db.execute(stmt)
    user_obj = result.one()[0]

    assert user_obj.username == "tester01"
    assert user_obj.email == "tester01@email.com"


@pytest.mark.asyncio
async def test_get_all_users(async_db: AsyncSession, async_client: AsyncClient):
    user1 = User(username="tester01", email="tester01@email.com", password_hash=generate_password_hash('123'))
    user2 = User(username="tester02", email="tester02@email.com", password_hash=generate_password_hash('123'))
    async_db.add(user1)
    async_db.add(user2)
    await async_db.commit()

    resp = await async_client.get('auth/get-all-users-v2')
    data = resp.json()

    assert resp.status_code == 200
    
    assert data[0]["id"] == user1.id
    assert data[0]["username"] == "tester01"
    assert data[0]["email"] == "tester01@email.com"

    assert data[1]["id"] == user2.id
    assert data[1]["username"] == "tester02"
    assert data[1]["email"] == "tester02@email.com"


@pytest.mark.asyncio
async def test_user_is_correct_isntance(async_db: AsyncSession, async_client: AsyncClient):
    user1 = User(username="tester01", email="tester01@email.com", password_hash=generate_password_hash('123'))
    async_db.add(user1)
    await async_db.commit()


    resp = await async_client.get(f'auth/get-user-v4/{user1.id}')
    data = resp.json()

    assert resp.status_code == 200
    assert isinstance(User(**data), User)
    assert data['email'] == user1.email


@pytest.mark.asyncio
async def test_auth_hashing(async_db: AsyncSession, async_client: AsyncClient):
    user1 = User(username="tester01", email="tester01@email.com", password_hash=generate_password_hash('123'))
    async_db.add(user1)
    await async_db.commit()

    assert verify_password("123", user1.password_hash)


@pytest.mark.asyncio
async def test_auth_create_user(async_db: AsyncSession, async_client: AsyncClient):
    data = {
        "username": "some_user",
        "email": "someuser@test.com",
        "password": "test123"
    }

    resp = await async_client.post('auth/signup-v3', json=data)

    assert resp.status_code == 201
    assert resp.json()[0] == 1

    user_id = resp.json()[0]

    resp = await async_client.get(f'auth/get-user-v4/{user_id}')
    data = resp.json()

    assert data["username"] == "some_user"
    assert data["email"] == "someuser@test.com"