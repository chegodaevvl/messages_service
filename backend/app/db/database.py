from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.core.settings import settings

db_url = settings.DATABASE_URL


async_engine = create_async_engine(db_url, echo=True)


async def get_async_session() -> AsyncSession:  # type: ignore
    async_session = async_sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
    await async_engine.dispose()
