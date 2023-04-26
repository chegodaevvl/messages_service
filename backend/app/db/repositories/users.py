from typing import List, Optional, Union

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.db.models import Follower, User
from app.models.users import FollowerInfo, UserCreate, UserDetail, UserInDB


class UserCRUD:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_apikey(self, api_key: str) -> Union[UserInDB, User]:
        select_stm = select(User).where(User.api_key == api_key)
        result = await self.session.execute(select_stm)
        user = result.scalars().first()
        if not user:
            return user  # type: ignore
        return UserInDB.from_orm(user)

    async def get_by_id(self, id: int) -> Union[UserInDB, Optional[User]]:
        select_stm = select(User).where(User.id == id)
        query_result = await self.session.execute(select_stm)
        user = query_result.scalars().first()
        if not user:
            return user
        return UserInDB.from_orm(user)

    async def get_followers(self, user_id: int) -> List[UserDetail]:
        select_stm = (
            select(Follower)
            .options(selectinload(Follower.follower))
            .where(Follower.following_id == user_id)
        )
        query_result = await self.session.execute(select_stm)
        followers = query_result.scalars().all()
        result = list()
        for follower in followers:
            result.append(UserDetail.from_orm(follower.follower))
        return result

    async def get_followings(self, user_id: int) -> List[UserDetail]:
        select_stm = (
            select(Follower)
            .options(selectinload(Follower.following))
            .where(Follower.follower_id == user_id)
        )
        query_result = await self.session.execute(select_stm)
        followers = query_result.scalars().all()
        result = list()
        for follower in followers:
            result.append(UserDetail.from_orm(follower.following))
        return result

    async def get_by_name(self, user_name: str) -> Optional[User]:
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
        select_stm = (
            select(Follower)
            .where(Follower.following_id == follow_link.following_id)
            .where(Follower.follower_id == follow_link.follower_id)
        )
        result = await self.session.execute(select_stm)
        if not result.scalars().first():
            return False
        return True

    async def add_follower(self, follower: FollowerInfo) -> bool:
        input_data = follower.dict()
        new_follower = Follower(**input_data)
        if await self.check_link(new_follower):
            return False
        self.session.add(new_follower)
        await self.session.commit()
        return True

    async def remove_follower(self, follower: FollowerInfo) -> bool:
        delete_stm = (
            delete(Follower)
            .where(Follower.following_id == follower.following_id)
            .where(Follower.follower_id == follower.follower_id)
        )
        await self.session.execute(delete_stm)
        await self.session.commit()
        return True
