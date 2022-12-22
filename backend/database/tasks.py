from fastapi import FastAPI
from databases import Database

from settings import DATABASE_URL


async def db_connect(app: FastAPI) -> None:
    database = Database(DATABASE_URL, min_size=2, max_size=10)

    await database.connect()
    app.state._db = database


async def db_disconnect(app: FastAPI) -> None:

    await app.state._db.disconnect()
