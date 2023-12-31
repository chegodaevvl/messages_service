from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_async_session
from app.db.repositories.media import MediaCRUD
from app.db.repositories.tweets import TweetCRUD
from app.db.repositories.users import UserCRUD


def get_user_crud(session: AsyncSession = Depends(get_async_session)) -> UserCRUD:
    return UserCRUD(session=session)


def get_tweet_crud(session: AsyncSession = Depends(get_async_session)) -> TweetCRUD:
    return TweetCRUD(session=session)


def get_media_crud(session: AsyncSession = Depends(get_async_session)) -> MediaCRUD:
    return MediaCRUD(session=session)
