from typing import Dict

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert

from app.db.models import User
from app.models.users import UserInDB, UserCreate


class UserCRUD:

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_apikey(self, api_key: str) -> UserInDB:
        select_stm = select(User).where(User.api_key == api_key)
        result = await self.session.execute(select_stm)
        user = result.scalars().first()
        if not user:
            return user
        return UserInDB.from_orm(user)

    async def get_by_id(self, id: int) -> UserInDB:
        select_stm = select(User).where(User.id == id)
        result = await self.session.execute(select_stm)
        user = result.scalars().first()
        if not user:
            return user
        return UserInDB.from_orm(user)

    async def bulk_add(self, users: list) -> None:
        add_stm = insert(User).values(users)
        await self.session.execute(add_stm)
        await self.session.commit()

    async def add_user(self, user: UserCreate) -> User:
        new_user = User(**user.dict())
        self.session.add(new_user)
        await self.session.commit()
        return new_user
