from fastapi import APIRouter


from src.apps.profiles.routes import router as profile_router
from src.apps.communities.router import router as community_router


apps_router = APIRouter(
    prefix='/apps'
)


apps_router.include_router(profile_router)
apps_router.include_router(community_router)

@apps_router.get('/')
async def apps_route_test():
    return "this is apps route"