import pytest

from httpx import AsyncClient
from fastapi import FastAPI

from starlette.status import HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY, HTTP_201_CREATED, HTTP_200_OK


pytestmark = pytest.mark.asyncio


class TestGetUser:

    async def test_get_user_by_id(self, app: FastAPI, client: AsyncClient) -> None:
        result = await client.get(app.url_path_for("users:get-user-by-id", id=1))
        assert result.status_code == HTTP_200_OK
        user = result.json()[0]
        assert user["id"] == 1

    async def test_get_current_user(self, app: FastAPI, client: AsyncClient) -> None:
        result = await client.get(app.url_path_for("users:get-current-user"))
        assert result.status_code == HTTP_200_OK
