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
from src.sections.authentication.hash import generate_password_hash, verify_password
from src.sections.authentication.utils import decode_token
from icecream import ic
ic.configureOutput(includeContext=True)

@pytest.mark.asyncio
async def test_auth_test_route(async_client: AsyncClient):
    resp = await async_client.get('auth/test')

    assert resp.status_code == 200
    assert resp.json()['message'] == "auth test route successful"


@pytest.mark.asyncio
async def test_auth_get_all_users(async_client: AsyncClient, sample_user):
    resp = await async_client.get('auth/get-all-users-v2')

    data = resp.json()

    assert data[0]["id"] == sample_user.id
    assert data[0]["username"] == sample_user.username
    assert data[0]["email"] == sample_user.email


@pytest.mark.asyncio
async def test_auth_get_all_users_no_data(async_client: AsyncClient):
    resp = await async_client.get('auth/get-all-users-v2')

    assert resp.status_code == 200
    assert resp.json() == []


@pytest.mark.asyncio
async def test_auth_get_all_users_v2_with_no_data(async_client: AsyncClient):
    resp = await async_client.get('auth/get-all-users-v2')

    assert resp.status_code == 200
    assert resp.json() == []



@pytest.mark.asyncio
async def test_auth_get_all_users_v2_with_data(async_db: AsyncSession, async_client: AsyncClient):
    new_user = User(username="tester01", email="tester01@email.com", password_hash=generate_password_hash('123'))
    async_db.add(new_user)
    await async_db.commit()

    resp = await async_client.get('auth/get-all-users-v2')

    assert resp.status_code == 200
    assert resp.json()[0]['username'] == new_user.username
    assert resp.json()[0]['email'] == new_user.email



@pytest.mark.asyncio
async def test_auth_get_user_object(async_db: AsyncSession, async_client: AsyncClient):
    new_user = User(username="tester01", email="tester01@email.com", password_hash=generate_password_hash('123'))
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
    new_user = User(username="tester01", email="tester01@email.com", password_hash=generate_password_hash('123'))
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
    new_user = User(username="tester01", email="tester01@email.com", password_hash=generate_password_hash('123'))
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
    new_user = User(username="tester01", email="tester01@email.com", password_hash=generate_password_hash('123'))
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


@pytest.mark.asyncio
async def test_auth_login(async_client: AsyncClient, sample_user):
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



@pytest.mark.asyncio
async def test_auth_user_profile_is_inaccissble(async_client: AsyncClient, sample_user):
    resp = await async_client.get("auth/me")

    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_auth_user_profile(async_client: AsyncClient, sample_user):
    data = {
        "email": "test01@email.com",
        "password": "test123"
    }

    resp = await async_client.post('auth/login', json=data)
    assert resp.status_code == 200

    login_data = resp.json()

    resp = await async_client.get('auth/me', headers={
        "Authorization": f"Bearer {login_data['access_token']}"
    })

    assert resp.status_code == 200
    data = resp.json()

    assert data["email"] == sample_user.email
    assert data["username"] == sample_user.username
    assert data["uid"] == str(sample_user.uid)


@pytest.mark.asyncio
async def test_auth_refresh_token_route(async_client: AsyncClient, sample_user):
    # aquire access and refresh token by logging in
    # blocklist the access token by logging out
    # re-aquire a fresh access token by using the refresh-token route
    # test if the new access token is valid by accessing profile route
    data = {
        "email": "test01@email.com",
        "password": "test123"
    }

    resp = await async_client.post('auth/login', json=data)
    assert resp.status_code == 200
    login_data = resp.json()

    resp = await async_client.post('auth/refresh-token', headers={
        "Authorization": f"Bearer {login_data['refresh_token']}"
    })

    new_access_token = resp.json()
    
    resp = await async_client.get('auth/me', headers={
        "Authorization": f"Bearer {new_access_token['access_token']}"
    })
    
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_auth_refresh_token_route_not_access_token(async_client: AsyncClient, sample_user):
    data = {
        "email": "test01@email.com",
        "password": "test123"
    }

    resp = await async_client.post('auth/login', json=data)
    assert resp.status_code == 200
    login_data = resp.json()

    resp = await async_client.post('auth/refresh-token', headers={
        "Authorization": f"Bearer {login_data['access_token']}"
    })

    assert resp.status_code == 403

    data = resp.json()
    assert data["error_code"] == 'refresh_token_required'
    assert data["message"] == "Please provide a valid refresh token"
    assert data["resolution"] == "Please get an refresh token"

@pytest.mark.asyncio
async def test_auth_refresh_token_route_invalid_token(async_client: AsyncClient, sample_user):
    data = {
        "email": "test01@email.com",
        "password": "test123"
    }

    resp = await async_client.post('auth/login', json=data)
    assert resp.status_code == 200
    login_data = resp.json()

    resp = await async_client.post('auth/refresh-token', headers={
        "Authorization": f"Bearer {login_data['refresh_token']}a"
    })

    assert resp.status_code == 401
    data = resp.json()
    assert data["error_code"] == 'invalid_token'
    assert data["message"] == "Token is invalid Or expired"
    assert data["resolution"] == "Please get new token"



@pytest.mark.asyncio
async def test_auth_logout_route(async_client: AsyncClient, sample_user):
    data = {
        "email": "test01@email.com",
        "password": "test123"
    }

    resp = await async_client.post('auth/login', json=data)
    assert resp.status_code == 200
    login_data = resp.json()

    resp = await async_client.get('auth/logout', headers={
        "Authorization": f"Bearer {login_data['access_token']}"
    })

    assert resp.status_code == 200
    data = resp.json()
    assert data["message"] == "Logged out successfully."


@pytest.mark.asyncio
async def test_auth_logout_route_refresh_token(async_client: AsyncClient, sample_user):
    data = {
        "email": "test01@email.com",
        "password": "test123"
    }

    resp = await async_client.post('auth/login', json=data)
    assert resp.status_code == 200
    login_data = resp.json()

    resp = await async_client.get('auth/logout', headers={
        "Authorization": f"Bearer {login_data['refresh_token']}"
    })

    assert resp.status_code == 401
    data = resp.json()
    assert data["message"] == "Please provide a valid access token"
    assert data["resolution"] == "Please get an access token"
    assert data["error_code"] == "access_token_required"


@pytest.mark.asyncio
async def test_auth_user_profile_v2(async_client: AsyncClient, sample_user):
    data = {
        "email": "test01@email.com",
        "password": "test123"
    }

    resp = await async_client.post('auth/login', json=data)
    assert resp.status_code == 200

    login_data = resp.json()

    resp = await async_client.get('auth/me-v2', headers={
        "Authorization": f"Bearer {login_data['access_token']}"
    })


@pytest.mark.asyncio
async def test_auth_user_profile_v3(async_client: AsyncClient, sample_user):
    data = {
        "email": "test01@email.com",
        "password": "test123"
    }

    resp = await async_client.post('auth/login', json=data)
    assert resp.status_code == 200

    login_data = resp.json()

    resp = await async_client.get('auth/me-v3', headers={
        "Authorization": f"Bearer {login_data['access_token']}"
    })


@pytest.mark.asyncio
async def test_auth_user_profile_v4(async_client: AsyncClient, sample_user):
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