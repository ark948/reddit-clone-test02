from icecream import ic
from typing import Optional, List
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
from backend.sections.database.models import Community
from backend.apps.communities import crud
from backend.apps.communities import search
from backend.sections.database.dependencies import AsyncSessionDep
from backend.sections.authentication.dependencies import getCurrentUserDep
from backend.apps.communities import actions
from backend.apps.communities import utils
from backend.apps.communities.dependencies import get_community_service_dep
from backend.apps.communities.service import CommunityService
from backend.apps.communities.schemas import (
    CommunityModel,
    CreateCommunity,
    CommunityModelCompact
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
    

@router.post('/leave/{community_id}', response_model=Dict, status_code=status.HTTP_200_OK)
async def leave_community(community_id: int, user: getCurrentUserDep, session: AsyncSessionDep):
    response = await actions.user_leave_community(community_id, user, session)
    if response:
        return {"message": "Successfully left community."}
    else:
        if len(user.communities) == 0:
            return {"message": "You are not a member of this community or community does not exist."}


@router.get('/user-joined-list', response_model=List, status_code=status.HTTP_200_OK)
async def get_list_of_joined_comms_for_current_user(user: getCurrentUserDep):
    # print("\n\n", type(user.communities), "\n\n")
    for community in user.communities:
        ic(community)
    return user.communities


@router.get('/members-count/{item_id}', response_model=int, status_code=status.HTTP_200_OK)
async def get_no_of_community_members(item_id: int, session: AsyncSessionDep):
    community_obj = await crud.get_community(item_id, session)
    members_count = len(community_obj.users)
    return members_count


@router.get('/joined-count', response_model=int, status_code=status.HTTP_200_OK)
async def get_no_of_communities_joined_by_user(user: getCurrentUserDep, session: AsyncSessionDep):
    return len(user.communities)


@router.get('/get-all', response_model=List[CommunityModelCompact], status_code=status.HTTP_200_OK)
async def get_all_communities(session: AsyncSessionDep):
    response = await crud.get_all(session)
    return response


@router.get('/check-joined/{community_id}', response_model=bool, status_code=status.HTTP_200_OK)
async def is_user_member(community_id: int, user: getCurrentUserDep):
    for community in user.communities:
        if community_id == community.id:
            return True
    return False