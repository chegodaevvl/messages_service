from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from app.core.settings import settings

db_url = settings.DATABASE_URL


async_engine = create_async_engine(db_url, echo=True)


async def get_async_session() -> AsyncSession:  # type: ignore
    """
    Функция инициализации сессии
    :return: AsyncSession - инициализированная сессия
    """
    async_session = async_sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
    await async_engine.dispose()
