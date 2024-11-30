from src.sections.database.provider import get_async_session
from typing import Annotated
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends





AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]