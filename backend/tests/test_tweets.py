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
        assert response["result"] is True

    async def test_remove_wrong_tweet(self,
                                      client: AsyncClient,
                                      test_user,
                                      test_tweet) -> None:
        result = await client.delete(f"api/tweets/{test_tweet.id + 100}", headers={"X-Token": test_user.api_key})
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert response["result"] is False
        assert response["error_type"] == "Not Found"
        assert response["error_message"] == "No tweet found with such id!"

    async def test_remove_not_owed_tweet(self,
                                         client: AsyncClient,
                                         second_user,
                                         test_tweet) -> None:
        result = await client.delete(f"api/tweets/{test_tweet.id}", headers={"X-Token": second_user.api_key})
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert response["result"] is False
        assert response["error_type"] == "Not Authorized"
        assert response["error_message"] == "You are unable to delete tweet, created by another user!"

    async def test_like_tweet(self,
                              client: AsyncClient,
                              test_tweet,
                              test_user,
                              second_user):
        result = await client.post(f"api/tweets/{test_tweet.id}/likes", headers={"X-Token": second_user.api_key})
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert response["result"] is True
        result = await client.post(f"api/tweets/{test_tweet.id}/likes", headers={"X-Token": test_user.api_key})
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert response["result"] is False

    async def test_like_tweet_not_exist(self,
                                        client: AsyncClient,
                                        test_tweet,
                                        second_user):
        result = await client.post(f"api/tweets/{test_tweet.id + 100}/likes", headers={"X-Token": second_user.api_key})
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert response["result"] is False
        assert response["error_type"] == "Not Found"
        assert response["error_message"] == "No tweet found with such id!"

    async def test_unlike_user(self,
                               client: AsyncClient,
                               test_tweet,
                               test_user,
                               second_user):
        result = await client.delete(f"api/tweets/{test_tweet.id}/likes", headers={"X-Token": second_user.api_key})
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert response["result"] is True
        result = await client.delete(f"api/tweets/{test_tweet.id}/likes", headers={"X-Token": second_user.api_key})
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert response["result"] is False
        result = await client.delete(f"api/tweets/{test_tweet.id}/likes", headers={"X-Token": test_user.api_key})
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert response["result"] is False
