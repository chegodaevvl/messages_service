import os
from fastapi import FastAPI
from databases import Database

from app.core.settings import DATABASE_URL


async def db_connect(app: FastAPI) -> None:
    db_url = f"""{DATABASE_URL}{os.environ.get("DB_SUFFIX", "")}"""
    database = Database(db_url, min_size=2, max_size=10)

    await database.connect()
    app.state._db = database


async def db_disconnect(app: FastAPI) -> None:

    await app.state._db.disconnect()
