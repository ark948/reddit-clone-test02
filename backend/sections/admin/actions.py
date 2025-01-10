

# meta actions reserved for admins:
# viewing of models and their fields
# editing model fields and information

# view all application routes

# view all current users

# view all active tokens
# modify all active tokens

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlmodel import select

from sections.database.connection import get_async_session
from sections.database.models import User


async def get_users_list(session: AsyncSession, order_by: str):
    stmt = select(User).filter_by(f"{order_by}")
    try:
        result = await session.scalars(stmt)
        return result.all()
    except Exception as error:
        return {
            "status": "ERROR",
            "detail": str(error)
        }
