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


    async def create_new_user(self, user_data: UserCreateModel) -> User | None:
        new_user_dict = user_data.model_dump()
        new_user = User(**new_user_dict)
        new_user.password_hash = genereate_password_hash(new_user_dict['password'])
        try:
            self.session.add(new_user)
            await self.session.commit()
            await self.session.refresh(new_user)
        except (IntegrityError, Exception) as error:
            print(error)
            return None
        return new_user
    

    async def get_user(self, user_id: int) -> User | None:
        try:
            user = await self.session.get(User, user_id)
        except Exception as error:
            print(error)
            return None
        
        return user
