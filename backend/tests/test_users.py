from typing import List
import pytest

from httpx import AsyncClient

from fastapi import status


pytestmark = pytest.mark.asyncio


class TestGetUser:

    async def test_users_wrong_secret(self,
                                      client: AsyncClient,
                                      users_data: List) -> None:
        result = await client.get(f"api/users/me")
        assert result.status_code == status.HTTP_200_OK
        # response = result.json()
        # assert response["result"] is False
        # assert response["error_type"] == "Permission denied"
        # assert response["error_message"] == "You're not authorized!"
