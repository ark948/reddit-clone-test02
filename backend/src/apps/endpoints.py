from fastapi import APIRouter


from src.apps.profiles.routes import router as profile_router
from src.apps.communities.router import router as community_router
from src.apps.posts.routes import router as posts_router
from src.apps.comments.router import router as comments_router


apps_router = APIRouter(
    prefix='/apps'
)


apps_router.include_router(profile_router)
apps_router.include_router(community_router)
apps_router.include_router(posts_router)
apps_router.include_router(comments_router)



@apps_router.get('/')
async def apps_route_test():
    return "this is apps route"