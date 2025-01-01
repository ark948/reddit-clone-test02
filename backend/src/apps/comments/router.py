from http import HTTPStatus
from pydantic import BaseModel
from fastapi import (
    APIRouter,
    HTTPException
)


# this app will contain everything in a single module, since it is not large enough



from src.sections.authentication.dependencies import getCurrentUserDep
from src.sections.database.dependencies import AsyncSessionDep
from src.sections.database.models import (
    Comment
)



router = APIRouter(
    prefix="/comments",
    tags=["Comment"]
)



class CommentModel(BaseModel):
    id: int
    content: str
    reactions: int
    author_id: int 
    post_id: int


class CreateComment(BaseModel):
    content: str



# test added
@router.get('/test')
async def comments_app_test():
    return "ok"



# test added
@router.get('/get/{item_id}', response_model=CommentModel | str, status_code=HTTPStatus.OK)
async def get_comment_by_id(item_id: int, session: AsyncSessionDep):
    try:
        commentObj = await session.get(Comment, item_id)
        if commentObj:
            return commentObj
        else:
            raise HTTPException(status_code=404)
    except Exception as error:
        print("ERROR in GET", error)
        raise HTTPException(status_code=404)


# test added
@router.post('/add/{post_id}', response_model=CommentModel, status_code=HTTPStatus.CREATED)
async def add_comment_to_post(post_id: int, comment_data: CreateComment , user: getCurrentUserDep, session: AsyncSessionDep):
    comment_data_dict = comment_data.model_dump()
    commentObj = Comment(content=comment_data_dict["content"], reactions=0, author_id=user.id, post_id=post_id)
    try:
        session.add(commentObj)
        await session.commit()
        return commentObj
    except Exception as error:
        print("ERROR IN comment: ", error)
        raise HTTPException(status_code=500, detail="Sorry, there was an error.")