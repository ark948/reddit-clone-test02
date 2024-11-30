import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from sqlalchemy.ext.asyncio import create_async_engine


# local imports
from src import app
from src.sections.database.dependencies import get_async_session
from src.sections.database.models import User


engine = create_async_engine(
    url='postgresql+asyncpg://...',
    echo=True,
)


@pytest.fixture(name='session_fixture')
def session_fixture():
    
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session



# will get session fixture
@pytest.fixture(name='client_fixture')
def client_fixture(session_fixture: Session):
    def get_session_override():
        return session_fixture
    app.dependency_overrides[get_async_session] = get_session_override
    client = TestClient(app=app)
    yield client
    app.dependency_overrides.clear()



@pytest.fixture(scope='session')
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()