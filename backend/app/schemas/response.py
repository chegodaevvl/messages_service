from typing import List, Optional

from app.schemas.core import BaseResponse
from app.schemas.tweets import TweetPublic
from app.schemas.users import UserPublic


class UserResponse(BaseResponse):
    """
    Модель ответа с информацией о пользователе
    """

    user: Optional[UserPublic]
    error_type: Optional[str]
    error_message: Optional[str]


class TweetResponse(BaseResponse):
    """
    Модель ответа с информацией о твите
    """

    tweet_id: Optional[int]
    error_type: Optional[str]
    error_message: Optional[str]


class MediaResponse(BaseResponse):
    """
    Модель ответа с информацией об изображении
    """

    media_id: Optional[int]
    error_type: Optional[str]
    error_message: Optional[str]


class TweetsResponse(BaseResponse):
    """
    Модель ответа со списоком твитов
    """

    tweets: Optional[List[TweetPublic]]
    error_type: Optional[str]
    error_message: Optional[str]
