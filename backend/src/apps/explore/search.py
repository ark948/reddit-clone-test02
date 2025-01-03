from fastapi import (
    APIRouter,
    status
)


router = APIRouter(
    prefix="/search"
)



from src.apps.posts import actions as posts_actions
from src.apps.tags.main import GetPostsWithTags, TagsList
from src.sections.database.dependencies import AsyncSessionDep




@router.get('/posts-by-tag', response_model=None, status_code=status.HTTP_200_OK)
async def search_posts_by_tag(list_of_tags: GetPostsWithTags, session: AsyncSessionDep):
    response = await posts_actions.select_posts_with_tags(list_of_tags, session)
    return response



@router.get('/posts-by-tags-v2', response_model=None, status_code=status.HTTP_200_OK)
async def get_posts_with_certain_tags_v2(list_of_tags: TagsList, session: AsyncSessionDep):
    response = await posts_actions.select_posts_with_tags_v2(list_of_tags, session)
    return response