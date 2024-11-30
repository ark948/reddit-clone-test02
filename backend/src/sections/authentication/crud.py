from sqlmodel import (
    insert
)


# local imports
from src.sections.database.dependencies import AsyncSessionDep
from src.sections.database.models import User
from src.sections.authentication.hash import genereate_password_hash
from src.sections.authentication.schemas import (
    UserCreateModel
)




async def create_user(user_data: UserCreateModel, session: AsyncSessionDep):
    new_user_dict = user_data.model_dump()
    new_user = User(**new_user_dict)
    new_user.password_hash = genereate_password_hash(new_user_dict['password'])
    try:
        session.add(new_user)
    except Exception as error:
        return {
            "status": "ERROR",
            "message": str(error)
        }
    await session.commit()
    return {
        "status": "SUCCESS",
        "user": new_user
    }
