from typing import Annotated
import pydantic
from fastapi import FastAPI, Body
from contextlib import asynccontextmanager


# local imports
from src.sections.database.provider import init_db
from src.sections.authentication.routes import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # not needed if alembic was added
    print("\n----> [Server - up] ---->\n")
    # await init_db()
    yield
    print("\n<---- [Server - down] <----\n")


app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)


@app.get('/test')
async def test_route():
    return {"message": "test successful"}

# to be able to send body request, either use pydantic model or Body from fastapi
class Message(pydantic.BaseModel):
    text: str

@app.post('/test')
async def test_post_route(message: Annotated[str, Body(embed=True)]):
    return {"input": message}