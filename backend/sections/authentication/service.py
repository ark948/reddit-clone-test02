from sqlmodel import select
from sqlalchemy.exc import IntegrityError
from typing import List, Union, Dict

# local imports
from backend.sections.database.dependencies import AsyncSessionDep
from backend.sections.database.models import User
from backend.sections.database.models import Profile
from backend.sections.authentication.schemas import UserCreateModel
from backend.sections.authentication.hash import generate_password_hash



class UserService:
    def __init__(self, session: AsyncSessionDep) -> None:
        self.session = session

    async def get_user(self, user_id: int) -> User | None:
        try:
            user = await self.session.get(User, user_id)
        except Exception as error:
            print(error)
            return None
        return user

    async def get_all_users(self) -> List[User] | None:
        try:
            stmt = select(User)
            users_list = await self.session.scalars(stmt)
        except Exception as error:
            print(error)
            return None
        return users_list.all()
    
    # auth mechanism
    async def get_user_by_email(self, email: str) -> Union[User, None]:
        try:
            stmt = select(User).where(User.email == email)
            user = await self.session.scalar(stmt)
        except Exception as error:
            print(error)
            return None
        return user
    
    async def user_exists(self, email: str) -> bool:
        user = await self.get_user_by_email(email)
        return True if user is not None else False

    async def create_new_user(self, user_data: UserCreateModel) -> Dict:
        new_user_dict = user_data.model_dump()
        new_user = User(**new_user_dict)
        new_user.role = "user"
        new_user.password_hash = generate_password_hash(new_user_dict['password'])
        try:
            self.session.add(new_user)
            await self.session.commit()
            await self.session.refresh(new_user)
        except (IntegrityError, Exception) as error:
            print(error)
            return None
        
        new_profile = Profile(user_id=new_user.id)
        try:
            self.session.add(new_profile)
            await self.session.commit()
        except Exception as error:
            print("\nERROR in creating profile\n", error)
        
        try:
            new_user.profile_id = new_profile.id
            await self.session.commit()
        except Exception as error:
            print("\nERROR in attaching profile to user\n", error)

        return {
            "user": new_user,
            "profile": new_profile
        }
    
    async def update_user(self, user: User, user_data: dict) -> Union[User, None]:
        for k, v in user_data.items():
            setattr(user, k, v)
        try:
            await self.session.commit()
            return user
        except (IntegrityError, Exception) as error:
            print(error)
            return None
