import pytest
from sqlalchemy.ext.asyncio.session import AsyncSession
from httpx import AsyncClient


from src.sections.database.models import Profile
from src.apps.profiles.schemas import UpdateProfile
from src.apps.profiles.crud import (
    get_profile,
    create_profile,
    update_profile
)


@pytest.mark.asyncio
async def test_profile_crud_get_profile(async_db: AsyncSession, sample_profile):
    profile_obj = await get_profile(sample_profile.id, sessino=async_db)

    assert isinstance(profile_obj, Profile) == True
    assert profile_obj.id == sample_profile.id
    assert profile_obj.first_name == "Mike"
    assert profile_obj.last_name == "Cobalt"


@pytest.mark.asyncio
async def test_profile_crud_create_profile(async_db: AsyncSession, sample_user):
    profile_obj = await create_profile(sample_user.id, async_db)
    
    assert profile_obj.id == 1
    assert isinstance(profile_obj, Profile) == True

@pytest.mark.asyncio
async def test_profile_crud_update_profile(async_db: AsyncSession, sample_profile):
    profile_update_model = UpdateProfile(first_name="John", last_name="Nolan")
    profile_obj = await update_profile(sample_profile.id, profile_update_model, async_db)

    assert profile_obj.first_name == "John"
    assert profile_obj.last_name == "Nolan"
    assert profile_obj.first_name == sample_profile.first_name
    assert profile_obj.last_name == sample_profile.last_name
    assert profile_obj.first_name != "Mike"
    assert sample_profile.last_name != "Cobalt"

