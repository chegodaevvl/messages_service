from typing import Callable
from fastapi import FastAPI

from database.tasks import db_connect, db_disconnect


def app_start_app_handler(app: FastAPI) -> Callable:
    async def start_app() -> None:
        await db_connect(app)

    return start_app


def app_stop_app_handler(app: FastAPI) -> Callable:
    async def stop_app() -> None:
        await db_disconnect(app)

    return stop_app
