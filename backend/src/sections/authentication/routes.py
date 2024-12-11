from typing import Dict, Union, List, Tuple, Annotated
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import timedelta, datetime
from sqlmodel import select, insert
from fastapi.responses import JSONResponse
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Body
)


# local imports
from src.sections import redis
from src.configs.settings import Config
from src.sections.database.models import User
from src.sections.database.dependencies import AsyncSessionDep
from src.sections.authentication import crud
from src.sections.mail import create_message, mail
from src.sections.authentication.roles import role_checker, getRoleCheckDep
from src.sections.authentication.service import UserService
from src.sections.database.provider import get_async_session
from src.sections.authentication.hash import generate_password_hash
from src.sections.authentication.tokens import AccessTokenBearer, RefreshTokenBearer
from src.sections.authentication.dependencies import (
    get_current_user, UserServiceDep, getCurrentUserDep
)
from src.sections.errors import (
    UserAlreadyExists, InvalidCredentials, InvalidToken, UserNotFound
)
from src.sections.authentication.utils import (
    create_access_token, decode_token, verify_password, create_url_safe_token, decode_url_safe_token
)
from src.sections.authentication.schemas import (
    UserCreateModel,
    UserModel,
    UserLoginModel,
    EmailModel,
    PasswordResetRequestModel,
    PasswordResetConfirmModel
)



router = APIRouter(prefix='/auth', tags=['auth'])
REFRESH_TOKEN_EXPIRY = 2



# test done
@router.get('/test')
async def auth_test():
    return {'message': "auth test route successful"}


@router.post('/send-mail')
async def send_mail(emails: EmailModel):
    emails = emails.addresses
    html = "<h1>Welcome to our app.</h1>"
    message = create_message(
        recipient=emails,
        subject="Welcome",
        body=html
    )
    await mail.send_message(message)
    return {
        "message": "Email sent successfully"
    }


# test done
@router.get('/get-all-users', response_model=List[UserModel], status_code=status.HTTP_200_OK)
async def get_all_users(session: AsyncSession=Depends(get_async_session)):
    resposne = await crud.get_all_users(session=session)
    return resposne



# test done
@router.get('/get-all-users-v2', response_model=List[UserModel], status_code=status.HTTP_200_OK)
async def get_all_users_v2(session: AsyncSession=Depends(get_async_session)):
    try:
        stmt = select(User)
        users = await session.scalars(stmt)
    except Exception as error:
        print(error)
        return None
    return users.all()



# test done
@router.get('/get-user/{user_id}', response_model=Union[User, None], status_code=status.HTTP_200_OK)
async def get_user_object(user_id: int, session: AsyncSessionDep):
    response = await crud.get_user(user_id=user_id, session=session)
    return response



# test done
@router.get('/get-user-v2/{user_id}', response_model=Union[User, None], status_code=status.HTTP_200_OK)
async def get_user_object_v2(user_id: int, u: UserServiceDep):
    response = await u.get_user(user_id=user_id)
    return response



# test done
@router.get('/get-user-v3/{user_id}', response_model=Union[UserModel, None], status_code=status.HTTP_200_OK)
async def get_user_object_v3(user_id: int, session: AsyncSession = Depends(get_async_session)):
    response = await crud.get_user_v2(user_id=user_id, session=session)
    return response



# test done
@router.get('/get-user-v4/{user_id}', response_model=Union[UserModel, None], status_code=status.HTTP_200_OK)
async def get_user_object_v4(user_id: int, session: AsyncSession=Depends(get_async_session)):
    try:
        stmt = select(User).where(User.id==user_id)
        user = await session.scalar(stmt)
    except Exception as error:
        print(error)
        return None
    return user



# test done
@router.post('/signup', response_model=UserModel, status_code=status.HTTP_201_CREATED)
async def create_user_account(user_data: UserCreateModel, session: AsyncSessionDep):
    response = await crud.create_user(user_data, session)
    if response:
        return response
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail="There was a problem, please check your input.")


# test done
@router.post('/signup-v2', response_model=UserModel, status_code=status.HTTP_201_CREATED)
async def create_user_account_v2(user_data: UserCreateModel, u: UserServiceDep):
    response = await u.create_new_user(user_data)
    if response:
        return response
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail="There was a problem, please check your input.")



# test done
# deprecated WARNING
@router.post('/signup-v3', response_model=Tuple, status_code=status.HTTP_201_CREATED)
async def create_user_account_v3(user_data: UserCreateModel, session: AsyncSession=Depends(get_async_session)):
    try:
        stmt = insert(User).values(username=user_data.username, email=user_data.email, password_hash=generate_password_hash(user_data.password))
        result = await session.execute(stmt)
        await session.commit()
    except Exception as error:
        print(error)
        return None
    return result.inserted_primary_key


@router.post('/signup-v4', response_model=Dict, status_code=status.HTTP_201_CREATED)
async def create_user_account_v4(user_data: UserCreateModel, session: AsyncSession=Depends(get_async_session)):
    user_service = UserService(session=session)
    email = user_data.email
    user_exists = await user_service.user_exists(email)
    if user_exists:
        raise UserAlreadyExists()
    new_user = await user_service.create_new_user(user_data)
    token = create_url_safe_token({"email": email})
    link = f"http://{Config.DOMAIN}/auth/verify/{token}"
    html_message = f"""
        <h1>Verify your email</h1>
        <p>Please click on this <a href="{link}">link</a> to verify your email</p>
        """
    try:
        message = create_message(
            recipient=[email],
            subject="Verify your email",
            body=html_message
        )
    except Exception as error:
        pass
    try:
        await mail.send_message(message)
    except Exception as error:
        pass
    print("\n\n", link, "\n\n")
    return {
        "message": "Account created. Check your email to verify your account.",
        "verify": link,
        "user": new_user
    }


@router.get('/verify/{token}')
async def verify_user_account(token: str, session: AsyncSession = Depends(get_async_session)):
    token_data = decode_url_safe_token(token)
    user_service = UserService(session=session)
    user_email = token_data.get('email')
    if user_email:
        user = await user_service.get_user_by_email(user_email)
        if not user:
            raise UserNotFound()
        await user_service.update_user(user, {'is_verified': True})
        return JSONResponse(content={
                "message": "User account successfully verified"
            }, status_code=status.HTTP_200_OK
        )
    return JSONResponse(content={
            "message": "Error occurred during verification"
        }, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )


# test done
@router.get('/me', response_model=Union[UserModel, None], status_code=status.HTTP_200_OK)
async def user_profile(session: AsyncSessionDep, user_data=Depends(AccessTokenBearer())):
    response = await crud.get_user_by_email(email=user_data["user"]["email"], session=session)
    return response

# test done
@router.get('/me-v2', response_model=Union[UserModel, None], status_code=status.HTTP_200_OK)
async def user_profile_v2(user=Depends(get_current_user), _: bool=Depends(role_checker)):
    return user

# test done
@router.get('/me-v3', response_model=Union[UserModel, None], status_code=status.HTTP_200_OK)
async def user_profile_v3(user: getCurrentUserDep, _: bool=Depends(role_checker)):
    return user

# test done
@router.get('/me-v4', response_model=Union[UserModel, None], status_code=status.HTTP_200_OK)
async def user_profile_v4(user: getCurrentUserDep, _: getRoleCheckDep):
    return user


# test done
# auth mechanism
@router.post('/refresh-token')
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details['exp']
    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(user_data=token_details["user"])
        return JSONResponse(content={"access_token": new_access_token})
    raise InvalidToken()



# test done
# auth mechanism
@router.post('/login', status_code=status.HTTP_200_OK)
async def login_users(login_data: UserLoginModel, session: AsyncSession = Depends(get_async_session)):
    email = login_data.email
    password = login_data.password
    user_service = UserService(session=session)
    user = await user_service.get_user_by_email(email)
    if user is not None:
        password_valid = verify_password(password, user.password_hash)
        if password_valid:
            access_token = create_access_token(
                user_data={
                    "email": user.email,
                    "user_uid": str(user.uid),
                    "role": user.role
                }
            )
            refresh_token = create_access_token(
                user_data={
                    "email": user.email,
                    "user_uid": str(user.uid)
                },
                refresh=True,
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY)
            )
            return JSONResponse(
                content={
                    "message": "Login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {
                        "email": user.email,
                        "uid": str(user.uid)
                    }
                }
            )
    raise InvalidCredentials()



@router.get('/logout', status_code=status.HTTP_200_OK)
async def revoke_token(token_details: dict = Depends(AccessTokenBearer())):
    jti = token_details['jti']
    await redis.add_jti_to_blocklist(jti)
    return JSONResponse(
        content={"message": "Logged out successfully."},
        status_code=status.HTTP_200_OK
    )