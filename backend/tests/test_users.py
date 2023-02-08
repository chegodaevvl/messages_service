from typing import List
import pytest

from httpx import AsyncClient

from fastapi import status


pytestmark = pytest.mark.asyncio


class TestGetUser:

    async def test_users_wrong_apikey(self,
                                      client: AsyncClient,
                                      test_user) -> None:
        result = await client.get(f"api/users/me", headers={"X-Token": "Invalid token"})
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert response["result"] is False
        assert response["error_type"] == "Permission denied"
        assert response["error_message"] == "You're not authorized!"

    async def test_get_current_user(self,
                                    client: AsyncClient,
                                    test_user) -> None:
        result = await client.get(f"api/users/me", headers={"X-Token": test_user.api_key})
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert response["result"] is True
        assert response["user"]["name"] == test_user.name

    async def test_get_user_by_id(self,
                                  client: AsyncClient,
                                  test_user) -> None:
        result = await client.get(f"api/users/{test_user.id}", headers={"X-Token": test_user.api_key})
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert response["result"] is True
        assert response["user"]["name"] == test_user.name

    async def test_get_user_by_wrong_id(self,
                                        client: AsyncClient,
                                        test_user):
        result = await client.get(f"api/users/{test_user.id + 1000}", headers={"X-Token": test_user.api_key})
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert response["result"] is False
        assert response["error_type"] == "Not Found"
        assert response["error_message"] == "No user found with such id!"

    async def test_follow_by_self(self,
                                     client: AsyncClient,
                                     test_user):
        result = await client.post(f"api/users/{test_user.id}/follow", headers={"X-Token": test_user.api_key})
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert response["result"] is False
        assert response["error_type"] == "Bad Request"
        assert response["error_message"] == "You couldn't follow yourself!"

    async def test_follow_user(self,
                               client: AsyncClient,
                               test_user,
                               second_user):
        result = await client.post(f"api/users/{second_user.id}/follow", headers={"X-Token": test_user.api_key})
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert response["result"] is True

    async def test_unfollow_user(self,
                                 client: AsyncClient,
                                 test_user,
                                 second_user):
        result = await client.delete(f"api/users/{second_user.id}/follow", headers={"X-Token": test_user.api_key})
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert response["result"] is True
