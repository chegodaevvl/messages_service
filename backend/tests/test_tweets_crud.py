import pytest

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from httpx import AsyncClient

from app.db.repositories.tweets import TweetCRUD
from app.db.models import Tweet
from app.models.users import UserCreate
from app.models.users import FollowerInfo


pytestmark = pytest.mark.asyncio


class TestTweetCrud:

    async def test_add_tweet(
            self,
            first_user,
            db: AsyncSession
    ) -> None:
        tweet_crud = TweetCRUD(db)
        new_tweet = {
            "tweet_data": "Test crud text",
            "user_id": first_user.id
        }
        result = await tweet_crud.add_tweet(new_tweet)
        assert result.id
        assert result.tweet_data == "Test crud text"
        delete_stm = delete(Tweet).where(Tweet.id == result.id)
        await db.execute(delete_stm)
        await db.commit()

    async def test_delete_tweet(
            self,
            first_tweet,
            db: AsyncSession
    ) -> None:
        tweet_crud = TweetCRUD(db)
        result = await tweet_crud.delete_tweet(first_tweet.id)
        assert result

    async def test_check_by_id(
            self,
            first_tweet,
            db: AsyncSession
    ) -> None:
        tweet_crud = TweetCRUD(db)
        result = await tweet_crud.check_by_id(first_tweet.id)
        assert result
        result = await tweet_crud.check_by_id(first_tweet.id + 1000)
        assert not result

    async def test_check_ownership(
            self,
            first_tweet,
            first_user,
            second_user,
            db: AsyncSession
    ) -> None:
        tweet_crud = TweetCRUD(db)
        result = await tweet_crud.check_ownership(first_tweet.id, first_user.id)
        assert result
        result = await tweet_crud.check_ownership(first_tweet.id, second_user.id)
        assert not result

    async def test_like_tweet(
            self,
            first_tweet,
            second_user,
            db: AsyncSession,
    ) -> None:
        tweet_crud = TweetCRUD(db)
        new_like = {
            "tweet_id": first_tweet.id,
            "user_id": second_user.id,
        }
        result = await tweet_crud.like_tweet(new_like)
        assert result

    async def test_check_tweet_like(
            self,
            first_tweet,
            second_user,
            first_user,
            db: AsyncSession,
            client: AsyncClient,
    ) -> None:
        tweet_crud = TweetCRUD(db)
        await client.post(f"api/tweets/{first_tweet.id}/likes", headers={"api-key": second_user.api_key})
        result = await tweet_crud.check_tweet_like(first_tweet.id, second_user.id)
        assert result
        result = await tweet_crud.check_tweet_like(first_tweet.id, first_user.id)
        assert not result

    async def test_unlike_tweet(
            self,
            first_tweet,
            second_user,
            db: AsyncSession,
    ) -> None:
        tweet_crud = TweetCRUD(db)
        new_like = {
            "tweet_id": first_tweet.id,
            "user_id": second_user.id,
        }
        result = await tweet_crud.unlike_tweet(new_like)
        assert result

    async def test_get_tweets(
            self,
            client: AsyncClient,
            db: AsyncSession,
            first_user,
            second_user,
            first_tweet,
            second_tweet,
    ) -> None:
        tweet_crud = TweetCRUD(db)
        result = await tweet_crud.get_tweets(first_user.id)
        assert len(result) == 0
        result = await tweet_crud.get_tweets(second_user.id)
        assert len(result) == 2
