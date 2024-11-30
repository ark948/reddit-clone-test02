from sqlalchemy.exc import IntegrityError
from typing import Dict

# local imports
from src.sections.database.dependencies import AsyncSessionDep
from src.sections.database.models import User
from src.sections.authentication.schemas import UserCreateModel
from src.sections.authentication.hash import genereate_password_hash



class UserService:
    def __init__(self, session: AsyncSessionDep) -> None:
        self.session = session


    async def create_new_user(self, user_data: UserCreateModel) -> Dict:
        new_user_dict = user_data.model_dump()
        new_user = User(**new_user_dict)
        new_user.password_hash = genereate_password_hash(new_user_dict['password'])
        try:
            self.session.add(new_user)
        except Exception as error:
            return {"status": "ERROR", "message": str(error)}
        try:
            await self.session.commit()
            await self.session.refresh(new_user)
        except IntegrityError as error:
            await self.session.rollback()
            return {"status": "ERROR", "message": str(error)}
        return {
            "status": "SUCCESS",
            "user": new_user
        }
