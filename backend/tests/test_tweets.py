from typing import List
import pytest

from httpx import AsyncClient

from fastapi import status


pytestmark = pytest.mark.asyncio


class TestTweet:

    async def test_add_tweet(self,
                             client: AsyncClient,
                             test_user) -> None:
        result = await client.post(f"api/tweets", headers={"X-Token": test_user.api_key})
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert response["result"] is True
        assert response["tweet_id"] == 1
