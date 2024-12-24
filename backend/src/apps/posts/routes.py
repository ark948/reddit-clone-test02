from typing import List
from fastapi import (
    APIRouter,
    status,
    HTTPException
)



# local imports
from src.apps.posts import schemas
from src.sections.authentication.dependencies import getCurrentUserDep
from src.sections.database.dependencies import AsyncSessionDep
from src.apps.posts.deps import postServiceDep
from src.apps.posts import actions



router = APIRouter(
    prefix="/posts",
    tags=["Post"]
)


@router.get('/test')
async def posts_app_test():
    return {
        "message": "posts app ok"
    }



@router.get('/get-post/{item_id}', response_model=schemas.PostModel | dict, status_code=status.HTTP_200_OK)
async def get_post(item_id: int, ps: postServiceDep):
    resposne = await ps.get_post(item_id)
    if resposne:
        return resposne
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No post with such id")


@router.post('/create-post/{community_id}', response_model=schemas.PostModel | dict, status_code=status.HTTP_201_CREATED)
async def create_post(community_id: int, user: getCurrentUserDep, post_data: schemas.CreatePost, session: AsyncSessionDep, ps: postServiceDep):
    for community in user.communities:
        if community_id == community.id:
            resposne = await ps.create_post(user.id, post_data, community_id)
            if resposne:
                return resposne
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not a member of this community or it does not exist.")


@router.get('/get-user-posts', response_model=List[schemas.PostModel], status_code=status.HTTP_200_OK)
async def all_posts_of_user(user: getCurrentUserDep):
    return user.posts



@router.get('/user-liked-posts/{post_id}', response_model=List[schemas.PostModel], status_code=status.HTTP_200_OK)
async def get_user_liked_posts(user: getCurrentUserDep, session: AsyncSessionDep):
    return user.likes



@router.post('/like-post/{post_id}', response_model=dict, status_code=status.HTTP_200_OK)
async def increase_post_reactions(post_id: int, user: getCurrentUserDep, session: AsyncSessionDep):
    resposne = await actions.user_like_post(post_id, user, session)
    if resposne:
        return {
            "message": "Like successful"
        }