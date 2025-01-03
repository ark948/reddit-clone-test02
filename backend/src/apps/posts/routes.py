from typing import List
from sqlmodel import select
from sqlalchemy.orm import joinedload
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
from src.sections.database.models import Post
from src.apps.comments.router import CommentModel
from src.apps.posts import crud
from src.apps.tags.main import GetPostsWithTags
from src.apps.posts.actions import TagsList



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



@router.get('/get-post-with-comments/{item_id}', response_model=List[CommentModel], status_code=status.HTTP_200_OK)
async def get_post_with_comments(item_id: int, ps: postServiceDep):
    resposne = await ps.get_post(item_id)
    if resposne:
        return resposne.comments
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No post with such id")


@router.get('/get-post-with-comments-v2/{item_id}', response_model=schemas.PostWithComments, status_code=status.HTTP_200_OK)
async def get_post_with_comments_v2(item_id: int, session: AsyncSessionDep):
    try:
        stmt = select(Post).options(joinedload(Post.comments)).where(Post.id==item_id)
        postObj = await session.scalar(stmt)
        return postObj
    except Exception as error:
        print("ERROR: ", error)
        raise HTTPException(status_code=500)
    

@router.get('/get-post-with-tags/{item_id}', response_model=schemas.PostWithTags, status_code=status.HTTP_200_OK)
async def get_post_with_tags(item_id: int, session: AsyncSessionDep):
    resposne = await crud.get_post(item_id, session)
    return resposne



@router.get('/get-post-with-tags-comments/{item_id}', response_model=schemas.PostWithTagsAndComments, status_code=status.HTTP_200_OK)
async def get_post_with_tags_and_comments(item_id: int, session: AsyncSessionDep):
    resposne = await crud.get_post(item_id, session)
    return resposne



@router.get('/get-posts-with-certain-tags', response_model=None, status_code=status.HTTP_200_OK)
async def get_posts_with_certain_tags(list_of_tags: GetPostsWithTags, session: AsyncSessionDep):
    response = await actions.select_posts_with_tags(list_of_tags, session)
    return response



@router.get('/get-posts-with-certain-tags-v2', response_model=None, status_code=status.HTTP_200_OK)
async def get_posts_with_certain_tags_v2(list_of_tags: TagsList, session: AsyncSessionDep):
    response = await actions.select_posts_with_tags_v2(list_of_tags, session)
    return response



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



@router.delete('/delete-post/{post_id}', response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, user: getCurrentUserDep, session: AsyncSessionDep, ps: postServiceDep):
    for post in user.posts:
        if post_id == post.id:
            response = await ps.delete_post(post_id, user.id)
            if response == 1:
                return None
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