import pytest
from httpx import AsyncClient


# local imports
from src.sections.authentication.utils import decode_token
from src.sections.redis import (
    token_in_blocklist,
    add_jti_to_blocklist
)



@pytest.mark.asyncio
async def test_redis_actions(async_client: AsyncClient, redis_client, sample_user):
    data = {
        "email": "test01@email.com",
        "password": "test123"
    }

    resp = await async_client.post('auth/login', json=data)
    assert resp.status_code == 200

    login_data = resp.json()
    token_data = decode_token(login_data['access_token'])

    await add_jti_to_blocklist(token_data["jti"], redis_client)

    response = await token_in_blocklist(token_data['jti'], redis_client)
    assert response == True


