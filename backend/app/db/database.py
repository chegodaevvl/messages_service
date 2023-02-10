from os import environ
from sys import modules

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.settings import settings

if "pytest" in modules:
    db_url = f"""{settings.DATABASE_URL}_test"""
else:
    db_url = settings.DATABASE_URL


async_engine = create_async_engine(db_url, echo=True, future=True)


async def get_async_session() -> AsyncSession:  # type: ignore
    async_session = sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
