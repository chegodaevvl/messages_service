import pytest

from httpx import AsyncClient
from fastapi import FastAPI

from fastapi import status

from app.models.users import UserInDB


pytestmark = pytest.mark.asyncio


class TestGetUser:

    async def test_get_user_by_id(self, app: FastAPI, client: AsyncClient, test_user: UserInDB) -> None:
        result = await client.get(app.url_path_for("users:get-user-by-id", id=test_user.id))
        assert result.status_code == status.HTTP_200_OK
        user = UserInDB(**result.json())
        assert user == test_user

    async def test_get_current_user(self, app: FastAPI, client: AsyncClient, test_user: UserInDB) -> None:
        result = await client.get(app.url_path_for("users:get-current-user", secret=test_user.access_key))
        user = UserInDB(**result.json())
        assert result.status_code == status.HTTP_200_OK
        assert user == test_user
