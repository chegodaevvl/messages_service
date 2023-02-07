from os import environ
from typing import List
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

from alembic import command
from alembic.config import Config

from app.db.database import async_engine
from app.db.repositories.users import UserCRUD
from app.db.models import User
from app.models.users import UserCreate, UserInDB


@pytest_asyncio.fixture(scope="session")
def apply_migrations():
    environ["DB_SUFFIX"] = "_test"
    config = Config("alembic.ini")
    command.upgrade(config, "head")
    yield
    command.downgrade(config, "base")


@pytest_asyncio.fixture(scope="function")
async def db() -> AsyncSession:
    async_session = sessionmaker(
        async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
    await async_engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def async_app() -> FastAPI:

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
async def test_user(db) -> User:

    user_crud = UserCRUD(db)
    test_user = UserCreate(name="Chosen One",
                           api_key="Superior")
    return await user_crud.add_user(test_user)
