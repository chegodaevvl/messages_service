import pytest

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.users import UserCRUD
from app.db.models import User
from app.models.users import UserCreate


pytestmark = pytest.mark.asyncio


class TestUserCRUD:

    async def test_add_user(
            self,
            db: AsyncSession
    ) -> None:
        user_crud = UserCRUD(db)
        new_user = UserCreate(name="New Chosen One",
                              api_key="NewSuperior")
        user_created = await user_crud.add_user(new_user)
        created_user_id = user_created.id
        assert user_created.name == new_user.name
        assert created_user_id
        user_created = await user_crud.add_user(new_user)
        assert user_created.id == created_user_id
        delete_stm = delete(User).where(User.id == user_created.id)
        await db.execute(delete_stm)
        await db.commit()

    async def test_get_by_apikey(
            self,
            db: AsyncSession,
            first_user,
    ) -> None:
        user_crud = UserCRUD(db)
        selected_user = await user_crud.get_by_apikey(first_user.api_key)
        assert selected_user.id == first_user.id
        assert selected_user.name == first_user.name
        selected_user = await user_crud.get_by_apikey("SomeSecret")
        assert not selected_user
