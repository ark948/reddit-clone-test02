import pytest


@pytest.mark.anyio
async def test_something():
    assert 1 == 1



@pytest.mark.anyio
async def test_another_thing():
    assert 1 == 1



@pytest.mark.anyio
async def test_this(ac):
    response = await ac.get('/test')
    
    assert response.status_code == 200

    data = response.json()
    assert data['message'] == "test successful"
