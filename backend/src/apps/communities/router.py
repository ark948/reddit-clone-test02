from typing import (
    List,
    Dict
)
from fastapi import (
    APIRouter,
    HTTPException,
    status
)


# local imports
from src.apps.communities import crud
from src.sections.database.dependencies import AsyncSessionDep
from src.sections.authentication.dependencies import getCurrentUserDep
from src.apps.communities.schemas import (
    CommunityModel,
    CreateCommunity
)


router = APIRouter(
    prefix='/community',
    tags=['community']
)


@router.get('/{item_id}', response_model=CommunityModel, status_code=status.HTTP_200_OK)
async def get_community(item_id: int, session: AsyncSessionDep):
    response = await crud.get_community(item_id, session)
    return response


@router.post('/', response_model=CommunityModel | None, status_code=status.HTTP_201_CREATED)
async def create_community(data: CreateCommunity, session: AsyncSessionDep):
    response = await crud.create_community(data, session)
    return response


@router.post('/join/{community_id}', response_model=Dict, status_code=status.HTTP_200_OK)
async def join_community(community_id: int, user: getCurrentUserDep, session: AsyncSessionDep):
    try:
        community_obj = await crud.get_community(community_id, session)
    except Exception as error:
        print(error)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    try:
        user.communities.append(community_obj)
    except Exception as error:
        print(error)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    try:
        await session.commit()
    except Exception as error:
        print("ERROR IN SAVE", error)
    return {
        "message": "Successfully joined.",
        "community": community_obj
    }