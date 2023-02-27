from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.users import UserCRUD
from app.db.database import get_async_session


def get_user_crud(
        session: AsyncSession = Depends(get_async_session)
) -> UserCRUD:
    return UserCRUD(session=session)