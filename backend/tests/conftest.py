import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool


# local imports
from src import app
from src.sections.database.dependencies import get_async_session
from src.sections.database.models import User


@pytest.fixture(name='session_fixture')
def session_fixture():
    engine = create_engine(
        # in-memory database
        "sqlite://", 
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
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