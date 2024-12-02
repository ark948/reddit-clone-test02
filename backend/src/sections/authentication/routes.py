from typing import Dict, Union, List, Tuple
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, insert
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)


# local imports
from src.sections.database.models import User
from src.sections.database.dependencies import AsyncSessionDep
from src.sections.authentication.schemas import UserCreateModel, UserModel
from src.sections.authentication import crud
from src.sections.authentication.dependencies import UserServiceDep
from src.sections.database.provider import get_async_session
from src.sections.authentication.hash import genereate_password_hash


router = APIRouter(prefix='/auth', tags=['auth'])


@router.get('/test')
async def auth_test():
    return {'message': "auth test route successful"}


# test SKIPPED (fixed) -> test added
# test not working (no exec command)
@router.get('/get-all-users', response_model=List[UserModel], status_code=status.HTTP_200_OK)
async def get_all_users(session: AsyncSession=Depends(get_async_session)):
    resposne = await crud.get_all_users(session=session)
    return resposne


# test done
@router.get('/get-all-users-v2', response_model=List[UserModel], status_code=status.HTTP_200_OK)
async def get_all_users_v2(session: AsyncSession=Depends(get_async_session)):
    try:
        stmt = select(User)
        users = await session.scalars(stmt)
    except Exception as error:
        print(error)
        return None
    return users.all()


# test done
@router.get('/get-user/{user_id}', response_model=Union[User, None], status_code=status.HTTP_200_OK)
async def get_user_object(user_id: int, session: AsyncSessionDep):
    response = await crud.get_user(user_id=user_id, session=session)
    return response

# test done
@router.get('/get-user-v2/{user_id}', response_model=Union[User, None], status_code=status.HTTP_200_OK)
async def get_user_object_v2(user_id: int, u: UserServiceDep):
    response = await u.get_user(user_id=user_id)
    return response

# test done
@router.get('/get-user-v3/{user_id}', response_model=Union[UserModel, None], status_code=status.HTTP_200_OK)
async def get_user_object_v3(user_id: int, session: AsyncSession = Depends(get_async_session)):
    response = await crud.get_user_v2(user_id=user_id, session=session)
    return response


# test done
@router.get('/get-user-v4/{user_id}', response_model=Union[UserModel, None], status_code=status.HTTP_200_OK)
async def get_user_object_v4(user_id: int, session: AsyncSession=Depends(get_async_session)):
    try:
        stmt = select(User).where(User.id==user_id)
        user = await session.scalar(stmt)
    except Exception as error:
        print(error)
        return None
    return user


# test done
@router.post('/signup', response_model=UserModel, status_code=status.HTTP_201_CREATED)
async def create_user_account(user_data: UserCreateModel, session: AsyncSessionDep):
    response = await crud.create_user(user_data, session)
    if response:
        return response
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail="There was a problem, please check your input.")


# test done
@router.post('/signup-v2', response_model=UserModel, status_code=status.HTTP_201_CREATED)
async def create_user_account_v2(user_data: UserCreateModel, u: UserServiceDep):
    response = await u.create_new_user(user_data)
    if response:
        return response
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail="There was a problem, please check your input.")


# test done
@router.post('/signup-v3', response_model=Tuple, status_code=status.HTTP_201_CREATED)
async def create_user_account_v3(user_data: UserCreateModel, session: AsyncSession=Depends(get_async_session)):
    try:
        stmt = insert(User).values(username=user_data.username, email=user_data.email, password_hash=genereate_password_hash(user_data.password))
        result = await session.execute(stmt)
        await session.commit()
    except Exception as error:
        print(error)
        return None
    return result.inserted_primary_key
