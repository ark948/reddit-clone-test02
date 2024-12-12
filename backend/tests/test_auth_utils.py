import pytest
from httpx import AsyncClient
from icecream import ic


from src.sections.authentication.hash import generate_password_hash, verify_password
from src.sections.authentication.utils import (
    create_access_token,
    decode_token
)




@pytest.mark.asyncio
async def test_generate_password_hash():
    plain_password = 'test123'
    password_hash = generate_password_hash(plain_password)

    assert password_hash != plain_password


@pytest.mark.asyncio
async def test_verify_password():
    plain_password = 'test123'
    password_hash = generate_password_hash(plain_password)

    assert verify_password(plain_password, password_hash) == True


@pytest.mark.asyncio
async def test_create_access_token(async_client: AsyncClient, sample_user):
    user_data = {
        "email": sample_user.email,
        "user_uid": str(sample_user.uid)
    }
    token = create_access_token(user_data)

    resp = await async_client.get('auth/me', headers={
        "Authorization": f"Bearer {token}"
    })

    assert resp.status_code == 200



@pytest.mark.asyncio
async def test_decode_token(async_client: AsyncClient, sample_user):
    user_data = {
        "email": sample_user.email,
        "user_uid": str(sample_user.uid)
    }

    token = create_access_token(user_data)

    data = decode_token(token)
    
    assert data['user']['email'] == sample_user.email
    assert data['user']['user_uid'] == str(sample_user.uid)