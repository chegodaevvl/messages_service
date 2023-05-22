from asyncio import run
from typing import List
from random import randint
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine

# from app.db.database import async_engine
from app.db.repositories.users import UserCRUD
from app.db.repositories.tweets import TweetCRUD
from app.models.users import UserCreate, UserInDB, FollowerInfo
from app.models.tweets import TweetCreate, TweetInDB, TweetLike

db_url = "postgresql+asyncpg://tweets_svr:tweets_pwd@db_server:5432/tweets_db"
async_engine = create_async_engine(db_url)
async_session = async_sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)


async def create_test_users() -> List[UserInDB]:
    users_list = list()
    async with async_session() as session:
        user_crud = UserCRUD(session)
        first_user = UserCreate(
            name="Ivan Ivanov",
            api_key="test"
        )
        users_list.append(await user_crud.add_user(first_user))
        second_user = UserCreate(
            name="Petr Petrov",
            api_key="test_word"
        )
        users_list.append(await user_crud.add_user(second_user))
        third_user = UserCreate(
            name="Sidor Sidorov",
            api_key="test_key"
        )
        users_list.append(await user_crud.add_user(third_user))
    return users_list


async def set_follow_relations(users: List[UserInDB]) -> None:
    async with async_session() as session:
        user_crud = UserCRUD(session)
        for i in range(2):
            new_follower = FollowerInfo(
                following_id=users[i+1].id,
                follower_id=users[0].id
            )
            await user_crud.add_follower(new_follower)
        new_follower = FollowerInfo(
            following_id=users[0].id,
            follower_id=users[2].id
        )
        await user_crud.add_follower(new_follower)


async def create_tweets(users: List[UserInDB]) -> List[TweetInDB]:
    tweets_list = list()
    async with async_session() as session:
        tweet_crud = TweetCRUD(session)
        for i in range(2):
            for j in range(4):
                new_tweet = TweetCreate(
                    tweet_data=f"Tweet number {(i + 1) * (j + 1)}",
                    user_id=users[i+1].id
                )
                tweets_list.append(await tweet_crud.add_tweet(new_tweet))
    return tweets_list


async def create_like_tweet(users: List[UserInDB], tweets: List[TweetInDB]) -> None:
    async with async_session() as session:
        tweet_crud = TweetCRUD(session)
        first_user_like = randint(0, 7)
        second_user_not_like = randint(4, 7)
        third_user_not_like = randint(0, 3)
        for i in range(8):
            if (i != third_user_not_like) and (i < 4):
                new_like = TweetLike(
                    tweet_id=tweets[i].id,
                    user_id=users[2].id
                )
            if (i != second_user_not_like) and (i < 4):
                new_like = TweetLike(
                    tweet_id=tweets[i].id,
                    user_id=users[1].id
                )
            await tweet_crud.like_tweet(new_like)
            if i == first_user_like:
                new_like = TweetLike(
                    tweet_id=tweets[i].id,
                    user_id=users[0].id
                )
                await tweet_crud.like_tweet(new_like)


async def generate_data() -> None:
    users = await create_test_users()
    print(users)
    tweets = await create_tweets(users)
    print(tweets)
    await set_follow_relations(users)
    await create_like_tweet(users, tweets)


run(generate_data())
