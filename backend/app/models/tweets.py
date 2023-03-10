from app.models.core import CoreModel, IDModelMixin


class TweetBase(CoreModel):
    tweet_data: str


class TweetCreate(TweetBase):
    user_id: int


class TweetInDB(IDModelMixin, TweetBase):
    pass

    class Config:
        orm_mode = True
