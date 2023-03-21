from typing import List
import pytest

from httpx import AsyncClient

from fastapi import status


pytestmark = pytest.mark.asyncio


class TestTweet:

    async def test_add_tweet(self,
                             client: AsyncClient,
                             test_user) -> None:
        test_tweet = {
            "tweet_data": "Test tweet message"
        }
        result = await client.post("api/tweets", headers={"X-Token": test_user.api_key}, json=test_tweet)
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert response["result"] is True
        assert response["tweet_id"] == 1

    async def test_remove_tweet(self,
                                client: AsyncClient,
                                test_user,
                                test_tweet) -> None:
        result = await client.delete(f"api/tweets/{test_tweet.id}", headers={"X-Token": test_user.api_key})
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        print(response)
        assert response["result"] is True
