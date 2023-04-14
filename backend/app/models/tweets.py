from typing import List
from app.models.core import CoreModel, IDModelMixin
from app.models.users import UserDetail
from app.models.media import MediaBase


class TweetBase(CoreModel):
    tweet_data: str


class TweetCreate(TweetBase):
    user_id: int


class TweetInDB(IDModelMixin, TweetBase):
    pass

    class Config:
        orm_mode = True


class TweetLike(CoreModel):
    tweet_id: int
    user_id: int


class TweetPublic(TweetInDB):
    attachments: List[MediaBase] = []
    author: UserDetail
    likes: List[UserDetail] = []

    class Config:
        orm_mode = True
