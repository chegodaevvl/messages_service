from os import path
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from httpx import AsyncClient

from fastapi import status
from app.db.repositories.media import MediaCRUD
from app.core.settings import settings


pytestmark = pytest.mark.asyncio


class TestTweet:

    async def test_add_tweet(self,
                             client: AsyncClient,
                             test_user) -> None:
        test_tweet = {
            "tweet_data": "Test tweet message"
        }
        result = await client.post("api/tweets", headers={"api-key": test_user.api_key}, json=test_tweet)
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert response["result"] is True
        assert response["tweet_id"] == 1

    async def test_remove_tweet(self,
                                client: AsyncClient,
                                test_user,
                                test_tweet,) -> None:
        result = await client.delete(f"api/tweets/{test_tweet.id}", headers={"api-key": test_user.api_key})
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert response["result"] is True

    async def test_remove_wrong_tweet(self,
                                      client: AsyncClient,
                                      test_user,
                                      test_tweet) -> None:
        result = await client.delete(f"api/tweets/{test_tweet.id + 100}", headers={"api-key": test_user.api_key})
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert response["result"] is False
        assert response["error_type"] == "Not Found"
        assert response["error_message"] == "No tweet found with such id!"

    async def test_remove_not_owed_tweet(self,
                                         client: AsyncClient,
                                         second_user,
                                         test_tweet) -> None:
        result = await client.delete(f"api/tweets/{test_tweet.id}", headers={"api-key": second_user.api_key})
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert response["result"] is False
        assert response["error_type"] == "Not Authorized"
        assert response["error_message"] == "You are unable to delete tweet, created by another user!"

    async def test_add_tweet_with_image(
            self,
            db: AsyncSession,
            client: AsyncClient,
            test_user,
            test_media,
    ) -> None:
        media_crud = MediaCRUD(db)
        images_ids = [test_media.id]
        test_tweet = {
            "tweet_data": "Test tweet message",
            "tweet_media_ids": images_ids
        }
        result = await client.post("api/tweets", headers={"api-key": test_user.api_key}, json=test_tweet)
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert response["result"] is True
        assert await media_crud.tweet_images_count(response["tweet_id"]) == 1
        images_ids = [test_media.id]
        test_tweet = {
            "tweet_data": "Test tweet message",
            "tweet_media_ids": images_ids
        }
        result = await client.post("api/tweets", headers={"api-key": test_user.api_key}, json=test_tweet)
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert response["result"] is False
        assert response["error_type"] == "Bad Request"
        assert response["error_message"] == "Wrong number of the tweet images!"
        images_ids = [test_media.id + 1000]
        test_tweet = {
            "tweet_data": "Test tweet message",
            "tweet_media_ids": images_ids
        }
        result = await client.post("api/tweets", headers={"api-key": test_user.api_key}, json=test_tweet)
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert response["result"] is False
        assert response["error_type"] == "Bad Request"
        assert response["error_message"] == "Wrong number of the tweet images!"

    async def test_like_tweet(self,
                              client: AsyncClient,
                              test_tweet,
                              test_user,
                              second_user):
        result = await client.post(f"api/tweets/{test_tweet.id}/likes", headers={"api-key": second_user.api_key})
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert response["result"] is True
        result = await client.post(f"api/tweets/{test_tweet.id}/likes", headers={"api-key": test_user.api_key})
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert response["result"] is False

    async def test_like_tweet_not_exist(self,
                                        client: AsyncClient,
                                        test_tweet,
                                        second_user):
        result = await client.post(f"api/tweets/{test_tweet.id + 100}/likes", headers={"api-key": second_user.api_key})
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert response["result"] is False
        assert response["error_type"] == "Not Found"
        assert response["error_message"] == "No tweet found with such id!"

    async def test_unlike_tweet(self,
                                client: AsyncClient,
                                test_tweet,
                                test_user,
                                second_user):
        await client.post(f"api/tweets/{test_tweet.id}/likes", headers={"api-key": second_user.api_key})
        result = await client.delete(f"api/tweets/{test_tweet.id}/likes", headers={"api-key": second_user.api_key})
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert response["result"] is True
        result = await client.delete(f"api/tweets/{test_tweet.id}/likes", headers={"api-key": second_user.api_key})
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert response["result"] is False
        result = await client.delete(f"api/tweets/{test_tweet.id}/likes", headers={"api-key": test_user.api_key})
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert response["result"] is False

    async def test_full_example(self,
                                db: AsyncSession,
                                client: AsyncClient,
                                test_user):
        media_crud = MediaCRUD(db)
        path_to_file = "tests/image.jpeg"
        images = {
            "image": open(path_to_file, "rb")
        }
        result = await client.post("api/media", headers={"api-key": test_user.api_key}, files=images)
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert response["result"] is True
        media_id = response["media_id"]
        assert path.exists(path.join(settings.MEDIA_PATH, f"image{media_id}.jpeg"))
        images_ids = [media_id]
        test_tweet = {
            "tweet_data": "Test tweet message",
            "tweet_media_ids": images_ids
        }
        result = await client.post("api/tweets", headers={"api-key": test_user.api_key}, json=test_tweet)
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        tweet_id = response["tweet_id"]
        assert response["result"] is True
        assert await media_crud.tweet_images_count(tweet_id) == 1
        result = await client.delete(f"api/tweets/{tweet_id}", headers={"api-key": test_user.api_key})
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert response["result"] is True
        assert await media_crud.tweet_images_count(tweet_id) == 0
        assert not path.exists(path.join(settings.MEDIA_PATH, f"image{media_id}.jpeg"))
