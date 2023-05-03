from typing import List, Optional

from app.models.core import CoreModel, IDModelMixin
from app.models.users import UserDetail


class TweetBase(CoreModel):
    """
    Базовая модель твита
    """
    tweet_data: str


class TweetCreate(TweetBase):
    """
    Модель сохдания твита
    """
    user_id: int


class TweetInDB(IDModelMixin, TweetBase):
    """
    Модель хранения твита в БД
    """
    pass

    class Config:
        orm_mode = True


class TweetLike(CoreModel):
    """
    Модель лайка твита
    """
    tweet_id: int
    user_id: int


class TweetPublic(IDModelMixin):
    """
    Полная модель твита
    """
    content: str
    attachments: List[str] = []
    author: UserDetail
    likes: List[UserDetail] = []

    class Config:
        orm_mode = True


class TweetImagesID(CoreModel):
    """
    Модель проверки перечня id изображений
    """
    tweet_images_id: Optional[List[int]]
