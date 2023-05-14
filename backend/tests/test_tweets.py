from os import path
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from httpx import AsyncClient

from fastapi import status
from sqlalchemy.future import select

from app.db.repositories.media import MediaCRUD
from app.db.repositories.tweets import TweetCRUD
from app.core.settings import settings
from app.db.models import Tweet


pytestmark = pytest.mark.asyncio


class TestTweet:

    async def test_create_tweet(self,
                                client: AsyncClient,
                                db: AsyncSession,
                                first_user) -> None:
        tweets_crud = TweetCRUD(db)
        first_tweet = {
            "tweet_data": "Test tweet message",
        }
        result = await client.post("api/tweets", headers={"api-key": first_user.api_key}, json=first_tweet)
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert response["result"]
        assert response["tweet_id"] == 3
        await tweets_crud.delete_all_tweets()
        wrong_tweet = {
            "tweet_data": ["Tweet text", 1, 34.9],
        }
        result = await client.post("api/tweets", headers={"api-key": first_user.api_key}, json=wrong_tweet)
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert not response["result"]
        assert response["error_type"] == "Bad Request"
        assert response["error_message"] == "Schema validation error! Not a string data provided!"
        wrong_tweet = {
            "tweet_data": "Tweet text",
            "tweet_media_ids": 12345987
        }
        result = await client.post("api/tweets", headers={"api-key": first_user.api_key}, json=wrong_tweet)
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert not response["result"]
        assert response["error_type"] == "Bad Request"
        assert response["error_message"] == "Schema validation error! Not a list of int provided!"
        wrong_tweet = {
            "tweet_data": "Tweet text",
            "tweet_media_ids": [1, "a", 0.7]
        }
        result = await client.post("api/tweets", headers={"api-key": first_user.api_key}, json=wrong_tweet)
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert not response["result"]
        assert response["error_type"] == "Bad Request"
        assert response["error_message"] == "Schema validation error! Not a list of int provided!"

    async def test_remove_tweet(self,
                                client: AsyncClient,
                                db: AsyncSession,
                                first_user,
                                first_tweet,) -> None:
        result = await client.delete(f"api/tweets/{first_tweet.id}", headers={"api-key": first_user.api_key})
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert response["result"]
        select_stm = select(Tweet).where(Tweet.id == first_tweet.id)
        query_result = await db.execute(select_stm)
        tweet = query_result.scalars().first()
        assert not tweet

    async def test_remove_wrong_tweet(self,
                                      client: AsyncClient,
                                      first_user,
                                      first_tweet) -> None:
        result = await client.delete(f"api/tweets/{first_tweet.id + 100}", headers={"api-key": first_user.api_key})
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert not response["result"]
        assert response["error_type"] == "Not Found"
        assert response["error_message"] == "No tweet found with such id!"

    async def test_remove_not_owed_tweet(self,
                                         client: AsyncClient,
                                         second_user,
                                         first_tweet) -> None:
        result = await client.delete(f"api/tweets/{first_tweet.id}", headers={"api-key": second_user.api_key})
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert not response["result"]
        assert response["error_type"] == "Not Authorized"
        assert response["error_message"] == "You are unable to delete tweet, created by another user!"

    async def test_create_tweet_with_image(
            self,
            db: AsyncSession,
            client: AsyncClient,
            first_user,
            test_media,
    ) -> None:
        media_crud = MediaCRUD(db)
        images_ids = [test_media.id, test_media.id + 1000]
        first_tweet = {
            "tweet_data": "Test tweet message",
            "tweet_media_ids": images_ids
        }
        result = await client.post("api/tweets", headers={"api-key": first_user.api_key}, json=first_tweet)
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert not response["result"]
        assert response["error_type"] == "Bad Request"
        assert response["error_message"] == "Wrong number of the tweet images!"
        images_ids = [test_media.id]
        first_tweet = {
            "tweet_data": "Test tweet message",
            "tweet_media_ids": images_ids
        }
        result = await client.post("api/tweets", headers={"api-key": first_user.api_key}, json=first_tweet)
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert response["result"]
        assert await media_crud.tweet_images_count(response["tweet_id"]) == 1
        images_ids = [test_media.id]
        first_tweet = {
            "tweet_data": "Test tweet message",
            "tweet_media_ids": images_ids
        }
        result = await client.post("api/tweets", headers={"api-key": first_user.api_key}, json=first_tweet)
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert not response["result"]
        assert response["error_type"] == "Bad Request"
        assert response["error_message"] == "Wrong number of the tweet images!"
        images_ids = [test_media.id + 1000]
        first_tweet = {
            "tweet_data": "Test tweet message",
            "tweet_media_ids": images_ids
        }
        result = await client.post("api/tweets", headers={"api-key": first_user.api_key}, json=first_tweet)
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert not response["result"]
        assert response["error_type"] == "Bad Request"
        assert response["error_message"] == "Wrong number of the tweet images!"

    async def test_like_tweet(self,
                              client: AsyncClient,
                              first_tweet,
                              first_user,
                              second_user):
        result = await client.post(f"api/tweets/{first_tweet.id}/likes", headers={"api-key": second_user.api_key})
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert response["result"]
        result = await client.post(f"api/tweets/{first_tweet.id}/likes", headers={"api-key": first_user.api_key})
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert not response["result"]

    async def test_like_tweet_not_exist(self,
                                        client: AsyncClient,
                                        first_tweet,
                                        second_user):
        result = await client.post(f"api/tweets/{first_tweet.id + 100}/likes", headers={"api-key": second_user.api_key})
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert not response["result"]
        assert response["error_type"] == "Not Found"
        assert response["error_message"] == "No tweet found with such id!"

    async def test_unlike_tweet(self,
                                client: AsyncClient,
                                first_tweet,
                                first_user,
                                second_user):
        await client.post(f"api/tweets/{first_tweet.id}/likes", headers={"api-key": second_user.api_key})
        result = await client.delete(f"api/tweets/{first_tweet.id}/likes", headers={"api-key": second_user.api_key})
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert response["result"]
        result = await client.delete(f"api/tweets/{first_tweet.id}/likes", headers={"api-key": second_user.api_key})
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert not response["result"]
        result = await client.delete(f"api/tweets/{first_tweet.id}/likes", headers={"api-key": first_user.api_key})
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert not response["result"]

    async def test_full_example(self,
                                db: AsyncSession,
                                client: AsyncClient,
                                first_user):
        media_crud = MediaCRUD(db)
        path_to_file = "tests/image.jpeg"
        images = {
            "image": open(path_to_file, "rb")
        }
        result = await client.post("api/media", headers={"api-key": first_user.api_key}, files=images)
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert response["result"]
        media_id = response["media_id"]
        assert path.exists(path.join(settings.MEDIA_PATH, f"image{media_id}.jpeg"))
        images_ids = [media_id]
        first_tweet = {
            "tweet_data": "Test tweet message",
            "tweet_media_ids": images_ids
        }
        result = await client.post("api/tweets", headers={"api-key": first_user.api_key}, json=first_tweet)
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        tweet_id = response["tweet_id"]
        assert response["result"]
        assert await media_crud.tweet_images_count(tweet_id) == 1
        result = await client.delete(f"api/tweets/{tweet_id}", headers={"api-key": first_user.api_key})
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert response["result"]
        assert await media_crud.tweet_images_count(tweet_id) == 0
        assert not path.exists(path.join(settings.MEDIA_PATH, f"image{media_id}.jpeg"))

    async def test_get_tweets(self,
                              client: AsyncClient,
                              db: AsyncSession,
                              first_tweet,
                              second_tweet,
                              first_user,
                              second_user,
                              test_media):
        media_crud = MediaCRUD(db)
        await client.post(f"api/users/{first_user.id}/follow", headers={"api-key": second_user.api_key})
        await client.post(f"api/tweets/{second_tweet.id}/likes", headers={"api-key": second_user.api_key})
        await media_crud.link_images_to_tweet(second_tweet.id, [test_media.id])
        result = await client.get(f"api/tweets", headers={"api-key": second_user.api_key})
        assert result.status_code == status.HTTP_200_OK
        response = result.json()
        assert response["result"]
        tweets_list = response["tweets"]
        assert len(tweets_list) == 2
        tweet = tweets_list[0]
        assert tweet["id"] == second_tweet.id
        assert tweet["content"] == second_tweet.tweet_data
        attachments = tweet["attachments"]
        assert len(attachments) == 1
        assert attachments[0] == test_media.link
        author = tweet["author"]
        assert author["id"] == first_user.id
        assert author["name"] == first_user.name
        likers = tweet["likes"]
        assert len(likers) == 1
        assert likers[0]["id"] == second_user.id
        assert likers[0]["name"] == second_user.name
        tweet = tweets_list[1]
        assert tweet["id"] == first_tweet.id
        assert tweet["content"] == first_tweet.tweet_data
        attachments = tweet["attachments"]
        assert len(attachments) == 0
        author = tweet["author"]
        assert author["id"] == first_user.id
        assert author["name"] == first_user.name
        await client.delete(f"api/users/{first_user.id}/follow", headers={"api-key": second_user.api_key})
