from os import environ

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.settings import settings

db_url = f"""{settings.DATABASE_URL}{environ.get("DB_SUFFIX", "")}"""


async_engine = create_async_engine(db_url, echo=True, future=True)


async def get_async_session() -> AsyncSession:  # type: ignore
    async_session = sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
