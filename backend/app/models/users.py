from typing import List, Optional

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


class UserDetail(IDModelMixin, UserBase):
    pass

    class Config:
        orm_mode = True


class UserPublic(UserDetail):
    followers: Optional[List[UserDetail]]
    following: Optional[List[UserDetail]]


class FollowerInfo(CoreModel):
    following_id: int
    follower_id: int
