from typing import List, Optional

from app.models.core import BaseResponse
from app.models.tweets import TweetPublic
from app.models.users import UserPublic


class UserResponse(BaseResponse):
    user: Optional[UserPublic]
    # error_type: Optional[str]
    # error_message: Optional[str]


class TweetResponse(BaseResponse):
    tweet_id: Optional[int]
    # error_type: Optional[str]
    # error_message: Optional[str]


class MediaResponse(BaseResponse):
    media_id: Optional[int]
    # error_type: Optional[str]
    # error_message: Optional[str]


class TweetsResponse(BaseResponse):
    tweets: Optional[List[TweetPublic]]
    # error_type: Optional[str]
    # error_message: Optional[str]
