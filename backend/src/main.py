from fastapi import FastAPI
from src.sections.database.provider import init_db
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # not needed if alembic was added
    print("\n----> [Server - up] ---->\n")
    await init_db()
    yield
    print("\n<---- [Server - down] <----\n")


app = FastAPI(
    lifespan=lifespan
)


@app.get('/test')
async def test_route():
    return {"message": "test successful"}
