import pytest
from sqlalchemy.ext.asyncio.session import AsyncSession


from src.sections.database.models import User
from src.sections.authentication.hash import verify_password
from src.sections.authentication.service import UserService
from src.sections.authentication.schemas import UserCreateModel
from icecream import ic
ic.configureOutput(includeContext=True)



@pytest.mark.asyncio
async def test_user_init(async_db: AsyncSession):
    u = UserService(session=async_db)

    assert isinstance(u, UserService)


@pytest.mark.asyncio
async def test_user_service_create_user(async_db: AsyncSession):
    u = UserService(session=async_db)
    new_user_data = UserCreateModel(username="tester01", email="tester01@email.com", password="test1234")
    result = await u.create_new_user(new_user_data)

    assert result.id == 1
    assert result.email == new_user_data.email
    assert result.username == new_user_data.username
    assert isinstance(result, User)


@pytest.mark.asyncio
async def test_user_service_create_user_password(async_db: AsyncSession):
    u = UserService(session=async_db)
    new_user_data = UserCreateModel(username="tester01", email="tester01@email.com", password="test1234")
    result = await u.create_new_user(new_user_data)

    assert hasattr(result, 'password') == False
    assert result.password_hash != new_user_data.password
    assert verify_password(new_user_data.password, result.password_hash) == True


@pytest.mark.asyncio
async def test_user_service_get_user(async_db: AsyncSession):
    u = UserService(session=async_db)
    new_user_data = UserCreateModel(username="tester01", email="tester01@email.com", password="test1234")
    result = await u.create_new_user(new_user_data)

    user_obj = await u.get_user(result.id)

    assert user_obj.id == result.id
    assert user_obj.username == "tester01"
    assert isinstance(user_obj, User)



@pytest.mark.asyncio
async def test_user_service_get_user_not_exist(async_db: AsyncSession):
    u = UserService(session=async_db)
    result = await u.get_user(1)

    assert result == None



@pytest.mark.asyncio
async def test_user_service_get_all_users(async_db: AsyncSession):
    u = UserService(session=async_db)
    new_user_data1 = UserCreateModel(username="tester01", email="tester01@email.com", password="test1234")
    new_user_data2 = UserCreateModel(username="tester02", email="tester02@email.com", password="test1234")
    await u.create_new_user(new_user_data1)
    await u.create_new_user(new_user_data2)

    result = await u.get_all_users()
    
    assert type(result) == list
    assert result[0].id == 1
    assert result[1].id == 2
    assert result[0].username == "tester01"
    assert result[1].username == "tester02"



@pytest.mark.asyncio
async def test_user_service_get_user_from_fixture(async_db: AsyncSession, sample_user):
    u = UserService(session=async_db)
    user_obj = await u.get_user(1)

    assert user_obj.id == sample_user.id
    assert user_obj.username == sample_user.username
    assert isinstance(user_obj, User)
    assert verify_password('test123', user_obj.password_hash) == True
    assert verify_password('test123', sample_user.password_hash) == True