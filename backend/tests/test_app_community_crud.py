import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio.session import AsyncSession



from src.sections.database.models import Community
from src.apps.communities.schemas import (
    CreateCommunity
)
from src.apps.communities.crud import (
    create_community,
    get_community,
    get_all
)



@pytest.mark.asyncio
async def test_crud_create_community(async_db: AsyncSession):
    data = {
        "title": "New Community",
        "about": "This is a community for testing..."
    }

    data_schema_obj = CreateCommunity(**data)
    response = await create_community(data_schema_obj, async_db)

    assert isinstance(response, Community)
    assert response.id == 1
    assert response.title == data["title"]
    assert response.about == "This is a community for testing..."
    assert response.users == []
    assert response.posts == []


@pytest.mark.asyncio
async def test_crud_get_community(sample_community, async_db):
    response = await get_community(1, async_db)

    assert isinstance(response, Community)
    assert response.id == 1
    assert response.title == sample_community.title
    assert response.about == "Cool facts about technology."
    assert response.users == []
    assert response.posts == []


@pytest.mark.asyncio
async def test_crud_get_all(multiple_communities, async_db):
    response = await get_all(async_db)
    
    assert len(response) == 3
    assert response[0].id == 1
    assert response[1].title == "co 2"
    assert response[2].about == "about co 3"
    assert response[0].users == []
    assert isinstance(response[1], Community)