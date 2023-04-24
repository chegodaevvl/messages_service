import pytest

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.users import UserCRUD
from app.db.models import User
from app.models.users import UserCreate
from app.models.users import FollowerInfo


pytestmark = pytest.mark.asyncio


class TestUsersCrud:

    async def test_get_user_by_apikey(
            self,
            first_user,
            db: AsyncSession
    ) -> None:
        user_crud = UserCRUD(db)
        result = await user_crud.get_by_apikey(first_user.api_key)
        assert result.id == first_user.id
        assert result.name == first_user.name
        result = await user_crud.get_by_apikey("APIKeyNotExist")
        assert not result

    async def test_get_user_by_id(
            self,
            first_user,
            db: AsyncSession
    ) -> None:
        user_crud = UserCRUD(db)
        result = await user_crud.get_by_id(first_user.id)
        assert result.id == first_user.id
        assert result.name == first_user.name
        result = await user_crud.get_by_id(first_user.id + 1000)
        assert not result

    async def test_get_user_by_name(
            self,
            first_user,
            db: AsyncSession
    ) -> None:
        user_crud = UserCRUD(db)
        result = await user_crud.get_by_name(first_user.name)
        assert result.id == first_user.id
        assert result.name == first_user.name

    async def test_add_user(
            self,
            first_user,
            db: AsyncSession
    ) -> None:
        user_crud = UserCRUD(db)
        test_user = UserCreate(name="Chosen One",
                               api_key="Superior")
        result = await user_crud.add_user(test_user)
        assert result.id == first_user.id
        assert result.name == first_user.name
        test_user = UserCreate(name="Test One",
                               api_key="TestAPIKey")
        result = await user_crud.add_user(test_user)
        assert result.id
        assert result.name == test_user.name
        delete_stm = delete(User).where(User.id == result.id)
        await db.execute(delete_stm)
        await db.commit()

    async def test_check_link_not_exist(
            self,
            db: AsyncSession,
            first_user,
            second_user,
    ) -> None:
        user_crud = UserCRUD(db)
        new_follower = FollowerInfo(
            following_id=second_user.id, follower_id=first_user.id
        )
        result = await user_crud.check_link(new_follower)
        assert not result

    async def test_add_follower(
            self,
            db: AsyncSession,
            first_user,
            second_user,
    ) -> None:
        user_crud = UserCRUD(db)
        new_follower = FollowerInfo(
            following_id=second_user.id, follower_id=first_user.id
        )
        result = await user_crud.add_follower(new_follower)
        assert result
        result = await user_crud.add_follower(new_follower)
        assert not result

    async def test_check_link_exist(
            self,
            db: AsyncSession,
            first_user,
            second_user,
    ) -> None:
        user_crud = UserCRUD(db)
        new_follower = FollowerInfo(
            following_id=second_user.id, follower_id=first_user.id
        )
        result = await user_crud.check_link(new_follower)
        assert result

    async def test_get_followers(
            self,
            db: AsyncSession,
            first_user,
            second_user,
    ) -> None:
        user_crud = UserCRUD(db)
        result = await user_crud.get_followers(second_user.id)
        assert len(result) == 1
        result[0].name == first_user.name
        result = await user_crud.get_followers(first_user.id)
        assert len(result) == 0

    async def test_get_followings(
            self,
            db: AsyncSession,
            first_user,
            second_user,
    ) -> None:
        user_crud = UserCRUD(db)
        result = await user_crud.get_followings(first_user.id)
        assert len(result) == 1
        result[0].name == second_user.name
        result = await user_crud.get_followings(second_user.id)
        assert len(result) == 0

    async def test_remove_follower(
            self,
            db: AsyncSession,
            first_user,
            second_user,
    ) -> None:
        user_crud = UserCRUD(db)
        new_follower = FollowerInfo(
            following_id=second_user.id, follower_id=first_user.id
        )
        result = await user_crud.remove_follower(new_follower)
        assert result
        result = await user_crud.check_link(new_follower)
        assert not result
