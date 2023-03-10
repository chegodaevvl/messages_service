from typing import Optional
from app.models.core import BaseResponse
from app.models.users import UserPublic


class UserResponse(BaseResponse):
    user: Optional[UserPublic]
    error_type: Optional[str]
    error_message: Optional[str]


class TweetResponse(BaseResponse):
    tweet_id: int
    error_type: Optional[str]
    error_message: Optional[str]
