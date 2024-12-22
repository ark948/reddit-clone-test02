from fastapi import (
    APIRouter,
    status,
    Depends
)



# local imports
from src.apps.posts import schemas
from src.sections.authentication.dependencies import getCurrentUserDep
from src.sections.database.dependencies import AsyncSessionDep
from src.apps.posts.deps import postServiceDep



router = APIRouter(
    prefix="/posts",
    tags=["Post"]
)


@router.get('/test')
async def posts_app_test():
    return {
        "message": "posts app ok"
    }



@router.get('/get-post/{item_id}', response_model=schemas.PostModel | None, status_code=status.HTTP_200_OK)
async def get_post(item_id: int, ps: postServiceDep):
    resposne = await ps.get_post(item_id)
    return resposne


@router.post('/create-post', response_model=schemas.PostModel | None, status_code=status.HTTP_201_CREATED)
async def create_post(user: getCurrentUserDep, post_data: schemas.CreatePost, session: AsyncSessionDep, ps: postServiceDep):
    resposne = await ps.create_post(user.id, post_data)
    return resposne

