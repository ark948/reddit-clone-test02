import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio.session import AsyncSession



class TestUserServiceClass:
    @classmethod
    def setup_method(cls, method):
        pass


    @classmethod
    def teardown_method(cls, method):
        pass


    @pytest.mark.asyncio
    async def test_main_test_route(self,  async_client: AsyncClient):
        resp = await async_client.get('/test')
        
        assert resp.status_code == 200
        assert resp.json()['message'] == "test successful"

    @pytest.mark.asyncio
    async def test_main_test_post_route(self, async_client: AsyncClient):
        resp = await async_client.post('/test', json={"text": "hello"})

        assert resp.status_code == 200
        assert resp.json()['input'] == "hello"