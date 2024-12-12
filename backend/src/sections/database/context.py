from contextlib import asynccontextmanager
from sqlalchemy.exc import IntegrityError


from src.sections.database.provider import get_async_session
from src.sections.authentication.schemas import UserCreateModel
from src.sections.errors import UserAlreadyExists
from src.sections.database.models import User
from src.sections.authentication.hash import generate_password_hash



get_async_session_context = asynccontextmanager(get_async_session)



async def create_user(username: str, email: str, password: str):
    try:
        async with get_async_session_context() as session:
            new_user = User(username=username, email=email, password_hash=generate_password_hash(password))
            new_user.role = "user"
            session.add(new_user)
            await session.commit()
            print("User created successfully.")
            return new_user
    except Exception as error:
        print(error)
        return None
        