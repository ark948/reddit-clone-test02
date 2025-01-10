from typing import Optional, List
from pydantic import BaseModel
from fastapi import (
    APIRouter,
    status
)


router = APIRouter(
    prefix="/search"
)



from backend.apps.posts import search as posts_search
from backend.apps.tags.main import GetPostsWithTags, TagsList
from backend.sections.database.dependencies import AsyncSessionDep
from backend.apps.communities import search as community_search
from backend.apps.communities.schemas import CommunityModelForSearch, CommunitySearchData




@router.get('/posts-by-tag', response_model=None, status_code=status.HTTP_200_OK)
async def search_posts_by_tag(list_of_tags: GetPostsWithTags, session: AsyncSessionDep):
    response = await posts_search.select_posts_with_tags(list_of_tags, session)
    return response



@router.get('/posts-by-tags-v2', response_model=None, status_code=status.HTTP_200_OK)
async def get_posts_with_certain_tags_v2(list_of_tags: TagsList, session: AsyncSessionDep):
    response = await posts_search.select_posts_with_tags_v2(list_of_tags, session)
    return response




@router.get('/community', response_model=Optional[List[CommunityModelForSearch]], status_code=status.HTTP_200_OK)
async def search_community(search_data: CommunitySearchData, session: AsyncSessionDep):
    response = await community_search.search_community_by_title(search_data.title, session)
    if response:
        return response