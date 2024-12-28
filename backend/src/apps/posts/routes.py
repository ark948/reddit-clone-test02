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
from src.apps.posts.dependencies import postServiceDep
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


@router.put('/edit-post/{post_id}', response_model=schemas.PostModel | dict, status_code=status.HTTP_200_OK)
async def edit_post(post_id: int, user: getCurrentUserDep, post_data: schemas.UpdatePost, session: AsyncSessionDep, ps: postServiceDep):
    for post in user.posts:
        if post_id == post.id:
            response = await ps.update_post(post_id, user.id, post_data)
            if response:
                return response
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Error, Post not found, or does not belong to you. Please check your input.")


@router.get('/get-user-posts', response_model=List[schemas.PostModel], status_code=status.HTTP_200_OK)
async def all_posts_of_user(user: getCurrentUserDep):
    return user.posts



@router.get('/user-liked-posts', response_model=List[schemas.PostModel], status_code=status.HTTP_200_OK)
async def get_user_liked_posts(user: getCurrentUserDep):
    return user.likes



@router.post('/like-post/{post_id}', response_model=dict, status_code=status.HTTP_200_OK)
async def add_user_like_post(post_id: int, user: getCurrentUserDep, session: AsyncSessionDep):
    resposne = await actions.user_like_post(post_id, user, session)
    if resposne:
        return resposne
    

@router.post('/remove-like-from-post/{post_id}', response_model=dict, status_code=status.HTTP_200_OK)
async def remove_user_like_from_post(post_id: int, user: getCurrentUserDep, session: AsyncSessionDep):
    resposne = await actions.user_remove_like_from_post(post_id, user, session)
    if resposne:
        return resposne



@router.get('/user-disliked-posts', response_model=List[schemas.PostModel], status_code=status.HTTP_200_OK)
async def get_user_disliked_posts(user: getCurrentUserDep):
    return user.dislikes


@router.post('/dislike-post/{post_id}', response_model=dict, status_code=status.HTTP_200_OK)
async def add_user_dislike_post(post_id: int, user: getCurrentUserDep, session: AsyncSessionDep):
    response = await actions.user_dislike_post(post_id, user, session)
    if response:
        return response
    

@router.post('/remove-dislike-from-post/{post_id}', response_model=dict, status_code=status.HTTP_200_OK)
async def remove_user_dislike_from_post(post_id: int, user: getCurrentUserDep, session: AsyncSessionDep):
    resposne = await actions.user_remove_dislike_from_post(post_id, user, session)
    if resposne:
        return resposne