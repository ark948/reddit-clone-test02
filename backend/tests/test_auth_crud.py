import pytest
from sqlalchemy.ext.asyncio.session import AsyncSession

from icecream import ic
ic.configureOutput(includeContext=True)

# local imports
from src.sections.authentication import crud
from src.sections.authentication.schemas import UserCreateModel
from src.sections.database.models import User



@pytest.mark.asyncio
async def test_auth_crud_get_all_users(async_db: AsyncSession, multiple_users):
    results = await crud.get_all_users(async_db)
    
    assert len(results) == 3


@pytest.mark.asyncio
async def test_auth_crud_get_user(async_db: AsyncSession, sample_user):
    result = await crud.get_user(sample_user.id, async_db)

    assert result.id == sample_user.id
    assert result.username == sample_user.username
    assert result.email == sample_user.email


@pytest.mark.asyncio
async def test_auth_crud_get_user_v2(async_db: AsyncSession, sample_user):
    result = await crud.get_user_v2(sample_user.id, async_db)

    assert result.id == sample_user.id
    assert result.username == sample_user.username
    assert result.email == sample_user.email


@pytest.mark.asyncio
async def test_auth_crud_create_user(async_db: AsyncSession):
    new_user_data = UserCreateModel(username="tester01", email="tester01@email.com", password="test1234")
    result = await crud.create_user(new_user_data, async_db)

    assert result.id == 1
    assert result.email == new_user_data.email
    assert result.username == new_user_data.username
    assert isinstance(result, User)