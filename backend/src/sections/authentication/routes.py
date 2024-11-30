from typing import Dict
from fastapi import (
    APIRouter,
    status
)


# local imports
from src.sections.database.models import User
from src.sections.database.dependencies import AsyncSessionDep
from src.sections.authentication.schemas import UserCreateModel
from src.sections.authentication import crud


router = APIRouter(prefix='/auth', tags=['auth'])

@router.get('/test')
async def auth_test():
    return {'message': "auth test route successful"}



@router.post('/signup', response_model=Dict, status_code=status.HTTP_201_CREATED)
async def create_user_account(user_data: UserCreateModel, session: AsyncSessionDep):
    response = await crud.create_user(user_data, session)
    return response