from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete

from app.db.models import Tweet
from app.models.tweets import TweetCreate, TweetInDB
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
