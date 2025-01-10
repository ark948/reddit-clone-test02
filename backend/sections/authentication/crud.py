from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlmodel import (
    select
)


# local imports
from backend.sections.database.dependencies import AsyncSessionDep
from backend.sections.database.models import User
from backend.sections.authentication.hash import generate_password_hash
from backend.sections.authentication.schemas import (
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
    new_user.password_hash = generate_password_hash(new_user_dict['password'])
    try:
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
    except Exception as error:
        print(error)
        await session.rollback()
        return None
    
    return new_user

async def update_user(user: User, user_data: dict, session: AsyncSession) -> User | None:
        for k, v in user_data.items():
            setattr(user, k, v)
        try:
            await session.commit()
            return user
        except (IntegrityError, Exception) as error:
            print(error)
            return None
