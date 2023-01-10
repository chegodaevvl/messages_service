from os import environ

import pytest
from asgi_lifespan import LifespanManager

from fastapi import FastAPI
from httpx import AsyncClient
from databases import Database

from alembic import command
from alembic.config import Config


from app.models.users import UserInDB, UserBase
from app.db.repositories.users import UserRepository


@pytest.fixture(scope="session")
def apply_migrations():
    environ["DB_SUFFIX"] = "test"
    config = Config("alembic.ini")
    command.upgrade(config, "head")
    yield
    command.downgrade(config, "base")


@pytest.fixture
def app(apply_migrations) -> FastAPI:
    from app.api.main import start_app

    return start_app()


@pytest.fixture
def db(app: FastAPI) -> Database:
    return app.state._db


@pytest.fixture
async def test_user(db: Database) -> UserInDB:

    user_repo = UserRepository(db)
    new_user = UserBase(
        name="Test user", access_key="TestSecret",
    )

    return await user_repo.create_user(new_user=new_user)


@pytest.fixture
async def client(app: FastAPI) -> AsyncClient:
    async with LifespanManager(app):
        async with AsyncClient(
            app=app,
            base_url="http://testserver",
            headers={"Content-Type": "application/json"}
        ) as client:
            yield client
