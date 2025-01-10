from typing import Annotated
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends



from backend.sections.database.connection import get_async_session



AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]
