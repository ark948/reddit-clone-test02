from typing import Annotated
import pydantic
from fastapi import FastAPI, Body
from contextlib import asynccontextmanager


# local imports
from src.sections.database.provider import init_db
from src.sections.authentication.routes import router as auth_router
from src.sections.errors import register_all_errors
from src.sections.middlewares.cors import register_cors_middleware
from src.apps.endpoints import apps_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # not needed if alembic was added
    print("\n----> [Server - up] ---->\n")
    # await init_db()
    yield
    print("\n<---- [Server - down] <----\n")


app = FastAPI(lifespan=lifespan)
register_all_errors(app=app)
register_cors_middleware(app=app)
app.include_router(auth_router)
app.include_router(apps_router)


@app.get('/test')
async def test_route():
    return {"message": "test successful"}

# to be able to send body request, either use pydantic model or Body from fastapi
class Message(pydantic.BaseModel):
    text: str

@app.post('/test')
async def test_post_route(message: Annotated[str, Body(embed=True)]):
    return {"input": message}