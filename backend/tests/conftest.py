import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

from alembic import command
from alembic.config import Config

from app.db.database import async_engine
from app.db.repositories.users import UserCRUD
from app.db.repositories.tweets import TweetCRUD
from app.db.repositories.media import MediaCRUD
from app.db.models import User
from app.models.users import UserCreate, UserInDB
from app.models.tweets import TweetCreate, TweetInDB
from app.models.media import MediaCreate, MediaInDB


@pytest_asyncio.fixture(scope="session")
def apply_migrations():
    config = Config("alembic.ini")
    command.upgrade(config, "heads")
    yield
    command.downgrade(config, "base")


@pytest_asyncio.fixture(scope="function")
async def db() -> AsyncSession:
    async_session = async_sessionmaker(
        async_engine, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
    await async_engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def async_app(apply_migrations) -> FastAPI:

    from app.main import create_app

    return create_app()


@pytest_asyncio.fixture(scope="function")
async def client(async_app: FastAPI) -> AsyncClient:
    async with AsyncClient(
            app=async_app,
            base_url="http://testserver"
    ) as async_client:
        yield async_client


@pytest_asyncio.fixture(scope="function")
async def first_user(db) -> User:

    user_crud = UserCRUD(db)
    first_user = UserCreate(name="Chosen One",
                            api_key="Superior")
    return await user_crud.add_user(first_user)


@pytest_asyncio.fixture(scope="function")
async def second_user(db) -> User:

    user_crud = UserCRUD(db)
    second_user = UserCreate(name="Super Second",
                             api_key="JustASecret")
    return await user_crud.add_user(second_user)


@pytest_asyncio.fixture(scope="function")
async def first_tweet(db, first_user) -> TweetInDB:

    tweet_crud = TweetCRUD(db)
    first_tweet = {
        "tweet_data": "Test tweet text",
        "user_id": first_user.id
    }
    yield await tweet_crud.add_tweet(first_tweet)
    await tweet_crud.delete_all_tweets()


@pytest_asyncio.fixture(scope="function")
async def second_tweet(db, first_user) -> TweetInDB:

    tweet_crud = TweetCRUD(db)
    second_tweet = {
        "tweet_data": "This is a second tweet",
        "user_id": first_user.id
    }
    yield await tweet_crud.add_tweet(second_tweet)
    await tweet_crud.delete_all_tweets()


@pytest_asyncio.fixture(scope="function")
async def test_media(db) -> MediaInDB:

    media_crud = MediaCRUD(db)
    test_media = {
        "link": "image.jpeg",
    }
    return await media_crud.upload_image(test_media)
