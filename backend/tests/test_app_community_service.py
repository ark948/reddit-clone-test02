import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio.session import AsyncSession



from src.sections.database.models import Community
from src.apps.communities.service import CommunityService


@pytest.mark.asyncio
async def test_community_service(async_db: AsyncSession, sample_community):
    response = await CommunityService(async_db).get_community(1)

    assert isinstance(response, Community)
    assert response.id == 1
    assert response.title == sample_community.title
    assert response.about == "Cool facts about technology."
    assert response.users == []
    assert response.posts == []