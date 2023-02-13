from typing import Dict

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert, delete

from app.db.models import User, Follower
from app.models.users import UserInDB, UserCreate, FollowerInfo


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

    async def get_by_name(self, user_name: str) -> User:
        select_stm = select(User).where(User.name == user_name)
        result = await self.session.execute(select_stm)
        user = result.scalars().first()
        return user

    async def add_user(self, user: UserCreate) -> User:
        new_user = await self.get_by_name(user.name)
        if new_user:
            return new_user
        new_user = User(**user.dict())
        self.session.add(new_user)
        await self.session.commit()
        return new_user

    async def check_link(self, follow_link: Follower):
        select_stm = select(Follower).where(
            Follower.user_id == follow_link.user_id
        ).where(
            Follower.follower_id == follow_link.follower_id
        )
        result = await self.session.execute(select_stm)
        if not result.scalars().first():
            return False
        return True

    async def add_follower(self, follower: FollowerInfo) -> bool:
        new_follower = Follower(**follower.dict())
        if await self.check_link(new_follower):
            return False
        self.session.add(new_follower)
        await self.session.commit()
        return True

    async def remove_follower(self, follower: FollowerInfo) -> bool:
        follower = Follower(**follower.dict())
        delete_stm = delete(Follower).where(
            user_id=follower.user_id,
            follower_id=follower.follower_id
        )
        await self.session.execute(delete_stm)
        await self.session.commit()
        return True
