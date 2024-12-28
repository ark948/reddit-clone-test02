import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio.session import AsyncSession



from src.sections.database.models import Post
from src.apps.posts.crud import (
    get_post
)



@pytest.mark.asyncio
async def test_crud_get_post(async_db, sample_post):
    postObj = await get_post(1, async_db)

    assert isinstance(postObj, Post) == True
    assert postObj.title == sample_post.title
    assert postObj.body == "And this is body."