from fastapi import APIRouter


from src.apps.profiles.routes import router as profile_router


apps_router = APIRouter(
    prefix='/apps'
)


apps_router.include_router(profile_router)