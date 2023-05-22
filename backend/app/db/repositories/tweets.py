from typing import Sequence

from sqlalchemy import delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.db.models import Follower, Like, Tweet
from app.models.tweets import TweetCreate, TweetInDB, TweetLike


class TweetCRUD:
    """
    Класс, описывающий CRUD действия с объектом Tweet
    """

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add_tweet(self, tweet: TweetCreate) -> TweetInDB:
        """
        Метод добавления нового твита
        :param tweet: TweetCreate - создаваемый твит
        :return: TweetInDB - Созданный твит
        """
        input_data = tweet.dict()
        new_tweet = Tweet(**input_data)
        self.session.add(new_tweet)
        await self.session.commit()
        return TweetInDB.from_orm(new_tweet)

    async def delete_tweet(self, tweet_id: int) -> bool:
        """
        Метод удаления твита
        :param tweet_id: int - id твита
        :return: bool - результат операции
        """
        delete_stm = delete(Tweet).where(Tweet.id == tweet_id)
        await self.session.execute(delete_stm)
        await self.session.commit()
        return True

    async def check_by_id(self, tweet_id: int) -> bool:
        """
        Метод проверки существования твита
        :param tweet_id: int - id твита
        :return: bool - результат проверки
        """
        select_stm = select(Tweet).where(Tweet.id == tweet_id)
        query_result = await self.session.execute(select_stm)
        tweet = query_result.scalars().first()
        if not tweet:
            return False
        return True

    async def check_ownership(self, tweet_id, user_id: int) -> bool:
        """
        Метод проверки авторства твита
        :param tweet_id: int - id твита
        :param user_id: int - id пользователя
        :return: bool - результат проверки
        """
        select_stm = (
            select(Tweet).where(Tweet.id == tweet_id).where(Tweet.user_id == user_id)
        )
        query_result = await self.session.execute(select_stm)
        tweet = query_result.scalars().first()
        if not tweet:
            return False
        return True

    async def like_tweet(self, tweet_like: TweetLike) -> bool:
        """
        Метод по проставлению лайка на твит
        :param tweet_like: TweetLike - объект лайка твита
        :return: bool - результат действия
        """
        input_data = tweet_like.dict()
        like_tweet = Like(**input_data)
        self.session.add(like_tweet)
        await self.session.commit()
        return True

    async def unlike_tweet(self, tweet_like: TweetLike) -> bool:
        """
        Метод по удалению лайка с твита
        :param tweet_like: TweetLike - объект лайка твита
        :return: bool - результат действия
        """
        delete_stm = (
            delete(Like)
            .where(Like.tweet_id == tweet_like.tweet_id)
            .where(Like.user_id == tweet_like.user_id)
        )
        await self.session.execute(delete_stm)
        await self.session.commit()
        return True

    async def check_tweet_like(self, tweet_id, user_id: int) -> bool:
        """
        Метод проверки что пользователь залайкал твит
        :param tweet_id: int - id твита
        :param user_id: int - id пользователя
        :return: bool - результат проверки
        """
        print(tweet_id)
        print(user_id)
        select_stm = (
            select(Like).where(Like.tweet_id == tweet_id).where(Like.user_id == user_id)
        )
        query_result = await self.session.execute(select_stm)
        like = query_result.scalars().first()
        print(like)
        if not like:
            return False
        return True

    async def get_tweets(self, user_id: int) -> Sequence[Tweet]:
        """
        Метод получения списка твитов для ленты пользователя
        :param user_id: int - id пользователя
        :return: список твитов для ленты пользователя
        """
        select_stm = (
            select(Tweet)
            .select_from(Like)
            .outerjoin(Tweet.likes)
            .group_by(Tweet.id)
            .order_by(func.count(Like.id).desc())
            .options(
                selectinload(Tweet.media),
                selectinload(Tweet.author),
                selectinload(Tweet.likes).subqueryload(Like.liker),
            )
            .where(
                Tweet.user_id.in_(
                    select(Follower.following_id).where(Follower.follower_id == user_id)
                )
            )
        )
        query_result = await self.session.execute(select_stm)
        tweets_list = query_result.scalars().all()
        return tweets_list

    async def delete_all_tweets(self) -> None:
        """
        Метод удаления всех твитов
        """
        delete_stm = delete(Tweet)
        await self.session.execute(delete_stm)
        await self.session.commit()
