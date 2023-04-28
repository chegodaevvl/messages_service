from typing import List, Optional

from app.models.core import CoreModel, IDModelMixin


class UserBase(CoreModel):
    """
    Базовая модель пользователя
    """
    name: str


class UserCreate(UserBase):
    """
    Модель создания пользователя
    """
    name: str
    api_key: str


class UserInDB(IDModelMixin, UserBase):
    """
    Модель хранения пользователя в БД
    """
    api_key: Optional[str]

    class Config:
        orm_mode = True


class UserDetail(IDModelMixin, UserBase):
    """
    Модель информации о пользователе
    """
    pass

    class Config:
        orm_mode = True


class UserPublic(UserDetail):
    """
    Полная модель пользователя
    """
    followers: Optional[List[UserDetail]]
    following: Optional[List[UserDetail]]


class FollowerInfo(CoreModel):
    """
    Модель отслеживания пользователя
    """
    following_id: int
    follower_id: int
