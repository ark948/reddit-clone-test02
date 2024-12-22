from fastapi import (
    APIRouter
)


router = APIRouter(
    prefix="/posts",
    tags=["Post"]
)


@router.get('/test')
async def posts_app_test():
    return {
        "message": "posts app ok"
    }