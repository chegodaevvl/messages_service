import asyncio
import pytest
import pytest_asyncio
from fastapi import FastAPI, Depends
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

from alembic import command
from alembic.config import Config

from app.core.settings import settings
from app.db.database import get_async_session
from app.db.repositories.users import UserCRUD
from app.db.repositories.tweets import TweetCRUD
from app.db.repositories.media import MediaCRUD
from app.db.models import User
from app.models.users import UserCreate, UserInDB
from app.models.tweets import TweetCreate, TweetInDB
from app.models.media import MediaCreate, MediaInDB


test_db_url = f"{settings.DATABASE_URL}_test"
test_db_engine = create_async_engine(test_db_url, echo=False)
async_session = async_sessionmaker(
    test_db_engine, expire_on_commit=False
)


async def get_test_session() -> AsyncSession:
    async with async_session() as session:
        yield session


def create_test_db() -> None:
    sync_engine = create_engine(settings.DATABASE_URL.replace("+asyncpg", ""))
    with sync_engine.connect() as test_connection:
        test_connection.exec_driver_sql("ROLLBACK")
        test_connection.exec_driver_sql(f"DROP DATABASE IF EXISTS {settings.POSTGRES_DB}_test")
        test_connection.exec_driver_sql(f"CREATE DATABASE {settings.POSTGRES_DB}_test")
    sync_engine.dispose()


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
def apply_migrations():
    config = Config("alembic.ini")
    create_test_db()
    test_sync_engine = create_engine(test_db_url.replace("+asyncpg", ""))
    config.attributes["connection"] = test_sync_engine
    command.upgrade(config, "heads")
    yield
    command.downgrade(config, "base")
    test_sync_engine.dispose()


@pytest_asyncio.fixture(scope="session")
async def db() -> AsyncSession:
    test_db = async_session()
    yield test_db
    await test_db.close()


@pytest_asyncio.fixture(scope="session")
async def async_app() -> FastAPI:

    from app.main import create_app
    app = create_app()
    app.dependency_overrides[get_async_session] = get_test_session
    yield app


@pytest_asyncio.fixture(scope="session")
async def client(async_app: FastAPI) -> AsyncClient:
    async with AsyncClient(
            app=async_app,
            base_url="http://testserver"
    ) as async_client:
        yield async_client


@pytest_asyncio.fixture(scope="session")
async def first_user(db) -> User:

    user_crud = UserCRUD(db)
    first_user = UserCreate(name="Chosen One",
                            api_key="Superior")
    return await user_crud.add_user(first_user)


@pytest_asyncio.fixture(scope="session")
async def second_user(db) -> User:

    user_crud = UserCRUD(db)
    second_user = UserCreate(name="Super Second",
                             api_key="JustASecret")
    return await user_crud.add_user(second_user)


@pytest_asyncio.fixture(scope="function")
async def first_tweet(db, first_user) -> TweetInDB:

    tweet_crud = TweetCRUD(db)
    first_tweet = TweetCreate(
        tweet_data="Test tweet text",
        user_id=first_user.id,
    )
    yield await tweet_crud.add_tweet(first_tweet)
    await tweet_crud.delete_all_tweets()


@pytest_asyncio.fixture(scope="function")
async def second_tweet(db, first_user) -> TweetInDB:

    tweet_crud = TweetCRUD(db)
    second_tweet = TweetCreate(
        tweet_data="This is a second tweet",
        user_id=first_user.id,
    )
    yield await tweet_crud.add_tweet(second_tweet)
    await tweet_crud.delete_all_tweets()


@pytest_asyncio.fixture(scope="function")
async def test_media(db) -> MediaInDB:

    media_crud = MediaCRUD(db)
    test_media = MediaCreate(
        link="image.jpeg",
    )
    return await media_crud.upload_image(test_media)
