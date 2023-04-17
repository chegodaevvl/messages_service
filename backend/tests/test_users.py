from typing import List
import pytest

from httpx import AsyncClient

from fastapi import status


pytestmark = pytest.mark.asyncio


class TestGetUser:

    async def test_users_wrong_apikey(self,
                                      client: AsyncClient,
                                      ) -> None:
        result = await client.get(f"api/users/me")
        assert result.status_code == status.HTTP_403_FORBIDDEN

    async def test_get_current_user(self,
                                    client: AsyncClient,
                                    first_user) -> None:
        result = await client.get(f"api/users/me", headers={"api-key": first_user.api_key})
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert response["result"] is True
        assert response["user"]["name"] == first_user.name

    async def test_get_user_by_id(self,
                                  client: AsyncClient,
                                  first_user) -> None:
        result = await client.get(f"api/users/{first_user.id}", headers={"api-key": first_user.api_key})
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert response["result"] is True
        assert response["user"]["name"] == first_user.name

    async def test_get_user_by_wrong_id(self,
                                        client: AsyncClient,
                                        first_user):
        result = await client.get(f"api/users/{first_user.id + 1000}", headers={"api-key": first_user.api_key})
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert response["result"] is False
        assert response["error_type"] == "Not Found"
        assert response["error_message"] == "No user found with such id!"

    async def test_follow_by_self(self,
                                  client: AsyncClient,
                                  first_user):
        result = await client.post(f"api/users/{first_user.id}/follow", headers={"api-key": first_user.api_key})
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert response["result"] is False
        assert response["error_type"] == "Bad Request"
        assert response["error_message"] == "It is unable to perform such operation on your own account!"

    async def test_follow_user(self,
                               client: AsyncClient,
                               first_user,
                               second_user):
        result = await client.post(f"api/users/{second_user.id}/follow", headers={"api-key": first_user.api_key})
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert response["result"] is True
        result = await client.post(f"api/users/{second_user.id}/follow", headers={"api-key": first_user.api_key})
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert response["result"] is False
        result = await client.get(f"api/users/{second_user.id}", headers={"api-key": first_user.api_key})
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert response["result"] is True
        assert "followers" in response["user"]
        assert len(response["user"]["followers"]) == 1
        assert response["user"]["followers"][0]["id"] == first_user.id
        assert response["user"]["followers"][0]["name"] == first_user.name
        result = await client.get(f"api/users/{first_user.id}", headers={"api-key": first_user.api_key})
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert response["result"] is True
        assert "following" in response["user"]
        assert len(response["user"]["following"]) == 1
        assert response["user"]["following"][0]["id"] == second_user.id
        assert response["user"]["following"][0]["name"] == second_user.name

    async def test_follow_user_not_exist(self,
                                         client: AsyncClient,
                                         first_user,
                                         second_user):
        result = await client.post(f"api/users/{second_user.id + 100}/follow", headers={"api-key": first_user.api_key})
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert response["result"] is False
        assert response["error_type"] == "Not Found"
        assert response["error_message"] == "No user found with such id!"

    async def test_unfollow_user(self,
                                 client: AsyncClient,
                                 first_user,
                                 second_user):
        result = await client.delete(f"api/users/{second_user.id}/follow", headers={"api-key": first_user.api_key})
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert response["result"] is True
