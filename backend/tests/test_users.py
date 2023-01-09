import pytest

from httpx import AsyncClient
from fastapi import FastAPI

from fastapi import status

from app.models.users import UserInDB


pytestmark = pytest.mark.asyncio


class TestGetUser:

    async def test_user_id_routes(self, app: FastAPI,
                          client: AsyncClient,
                          test_user: UserInDB) -> None:
        result = await client.get(app.url_path_for("users:get-user-by-id",
                                                   id=(test_user.id + 100)))
        response = result.json()
        assert result.status_code == status.HTTP_200_OK
        assert response["result"] is False
        assert response["error_type"] == "Not Found"
        assert response["error_message"] == "No user found with such id!"

    async def test_get_user_by_id(self, app: FastAPI,
                                  client: AsyncClient,
                                  test_user: UserInDB) -> None:
        result = await client.get(app.url_path_for("users:get-user-by-id",
                                                   id=test_user.id))
        response = result.json()
        assert result.status_code == status.HTTP_200_OK
        assert response["result"] is True
        user = UserInDB(**response["user"])
        assert user == test_user
