from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete

from app.db.models import Tweet, Like
from app.models.tweets import TweetCreate, TweetInDB, TweetLike
from sqlalchemy.orm import selectinload


class TweetCRUD:

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add_tweet(self, tweet: TweetCreate) -> TweetInDB:
        new_tweet = Tweet(**tweet)
        self.session.add(new_tweet)
        await self.session.commit()
        return TweetInDB.from_orm(new_tweet)

    async def delete_tweet(self, tweet_id: int) -> bool:
        delete_stm = delete(Tweet).where(
            Tweet.id == tweet_id
        )
        await self.session.execute(delete_stm)
        await self.session.commit()
        return True

    async def check_by_id(self, tweet_id: int) -> bool:
        select_stm = select(Tweet).where(Tweet.id == tweet_id)
        query_result = await self.session.execute(select_stm)
        tweet = query_result.scalars().first()
        if not tweet:
            return False
        return True

    async def check_ownership(self, tweet_id, user_id: int) -> bool:
        select_stm = select(Tweet).where(
            Tweet.id == tweet_id
        ).where(
            Tweet.user_id == user_id
        )
        query_result = await self.session.execute(select_stm)
        tweet = query_result.scalars().first()
        if not tweet:
            return False
        return True

    async def like_tweet(self, tweet_like: TweetLike) -> bool:
        tweet_like = Like(**tweet_like)
        self.session.add(tweet_like)
        await self.session.commit()
        return True

    async def unlike_tweet(self, tweet_like: TweetLike) -> bool:
        delete_stm = delete(Like).where(
            Like.tweet_id == tweet_like["tweet_id"]
        ).where(
            Like.user_id == tweet_like["user_id"]
        )
        await self.session.execute(delete_stm)
        await self.session.commit()
        return True

    async def check_tweet_like(self, tweet_id, user_id: int) -> bool:
        select_stm = select(Like).where(
            Like.tweet_id == tweet_id
        ).where(
            Like.user_id == user_id
        )
        query_result = await self.session.execute(select_stm)
        like = query_result.scalars().first()
        if not like:
            return False
        return True

    async def get_tweets(self):
        tweets_list = select(Tweet).options(selectinload(Tweet.medias))
        return tweets_list.scalars().all()
