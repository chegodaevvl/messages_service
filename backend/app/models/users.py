from typing import Optional
from app.models.core import CoreModel, IDModelMixin


class UserBase(CoreModel):
    name: str


class UserCreate(UserBase):
    name: str
    api_key: str


class UserInDB(IDModelMixin, UserBase):
    api_key: Optional[str]

    class Config:
        orm_mode = True


class UserPublic(IDModelMixin, UserBase):
    pass


class FollowerInfo(CoreModel):
    user_id: int
    follower_id: int
