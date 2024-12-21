from icecream import ic
ic.configureOutput(includeContext=True)
from typing import (
    List,
    Dict,
    Annotated,
    Union
)
from fastapi import (
    APIRouter,
    HTTPException,
    status,
    Body,
    Depends
)


# local imports
from src.sections.database.models import Community
from src.apps.communities import crud
from src.sections.database.dependencies import AsyncSessionDep
from src.sections.authentication.dependencies import getCurrentUserDep
from src.apps.communities import actions
from src.apps.communities.dependencies import get_community_service_dep
from src.apps.communities.service import CommunityService
from src.apps.communities.schemas import (
    CommunityModel,
    CreateCommunity,
)


router = APIRouter(
    prefix='/community',
    tags=['community']
)

@router.get('/test')
async def community_test_route():
    return 'community test route'

@router.get('/get-community/{item_id}', response_model=CommunityModel, status_code=status.HTTP_200_OK)
async def get_community(item_id: int, session: AsyncSessionDep):
    response = await crud.get_community(item_id, session)
    return response

@router.get('/get-community-v2', response_model=Union[CommunityModel, None], status_code=status.HTTP_200_OK)
async def get_community_v2(item_id: Annotated[int, Body(embed=True)], service: Annotated[CommunityService, Depends(get_community_service_dep)]):
    response = await service.get_community(item_id)
    return response if response else None


@router.post('/', response_model=CommunityModel | None, status_code=status.HTTP_201_CREATED)
async def create_community(data: CreateCommunity, session: AsyncSessionDep):
    response = await crud.create_community(data, session)
    return response


@router.post('/join/{community_id}', response_model=Dict, status_code=status.HTTP_200_OK)
async def join_community(community_id: int, user: getCurrentUserDep, session: AsyncSessionDep):
    resposne = await actions.user_join_community(community_id, user, session)
    if resposne:
        return {"message": "Successfully joined."}
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get('/user-joined-list', response_model=List, status_code=status.HTTP_200_OK)
async def get_list_of_joined_comms_for_current_user(user: getCurrentUserDep):
    return user.communities