from typing import List
import pytest

from httpx import AsyncClient

from fastapi import status


pytestmark = pytest.mark.asyncio


class TestGetUser:

    async def test_users_wrong_apikey(self,
                                      client: AsyncClient,
                                      users_data) -> None:

        result = await client.get(f"api/users/me", headers={"X-Token": "Invalid token"})
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert response["result"] is False
        assert response["error_type"] == "Permission denied"
        assert response["error_message"] == "You're not authorized!"

    async def test_get_current_user(self,
                                    client: AsyncClient,
                                    users_data) -> None:
        result = await client.get(f"api/users/me", headers={"X-Token": "Superior"})
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert response["result"] is True
        assert response["user"]["name"] == "Chosen One"

    async def test_get_user_by_id(self,
                                  client: AsyncClient,
                                  users_data) -> None:
        result = await client.get(f"api/users/2", headers={"X-Token": "Superior"})
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert response["result"] is True
        assert response["user"]["name"] == "Super Two"
        result = await client.get(f"api/users/20000", headers={"X-Token": "Superior"})
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert response["result"] is False
        assert response["error_type"] == "Not Found"
        assert response["error_message"] == "No user found with such id!"
