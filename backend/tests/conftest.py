import os

import pytest
from asgi_lifespan import LifespanManager

from fastapi import FastAPI
from httpx import AsyncClient
from databases import Database

from alembic import command
from alembic.config import Config


@pytest.fixture(scope="session")
def apply_migrations():
    os.environ["DB_SUFFIX"] = "test"
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
async def client(app: FastAPI) -> AsyncClient:
    async with LifespanManager(app):
        async with AsyncClient(
            app=app,
            base_url="http://testserver",
            headers={"Content-Type": "application/json"}
        ) as client:
            yield client
