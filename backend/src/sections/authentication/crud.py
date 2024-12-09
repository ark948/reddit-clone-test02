from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import IntegrityError
from typing import Dict
from sqlmodel import (
    select,
    insert
)


# local imports
from src.sections.database.dependencies import AsyncSessionDep
from src.sections.database.models import User
from src.sections.authentication.hash import genereate_password_hash
from src.sections.authentication.schemas import (
    UserCreateModel
)



async def get_all_users(session: AsyncSession):
    try:
        stmt = select(User)
        results = await session.scalars(stmt)
    except Exception as error:
        print(error)
        return None
    return results.all()


async def get_user(user_id: int, session: AsyncSessionDep) -> User | None:
    try:
        user = await session.get(User, user_id)
    except Exception as error:
        print(error)
        return None
    
    return user


async def get_user_v2(user_id: int, session: AsyncSession) -> User | None:
    try:
        user = await session.get(User, user_id)
    except Exception as error:
        print(error)
        return None
    
    return user

async def get_user_by_email(email: str, session: AsyncSessionDep) -> User | None:
    try:
        user = await session.scalar(select(User).where(User.email == email))
    except Exception as error:
        print(error)
        return None
    return user


async def create_user(user_data: UserCreateModel, session: AsyncSessionDep) -> User | None:
    new_user_dict = user_data.model_dump()
    new_user = User(**new_user_dict)
    new_user.role = "user"
    new_user.password_hash = genereate_password_hash(new_user_dict['password'])
    try:
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
    except Exception as error:
        print(error)
        await session.rollback()
        return None
    
    return new_user