from typing import Optional
from app.models.core import BaseResponse
from app.models.users import UserPublic


class UserResponse(BaseResponse):
    user: Optional[UserPublic]
