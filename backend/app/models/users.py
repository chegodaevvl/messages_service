from typing import Optional
from app.models.core import CoreModel, IDModelMixin


class UserBase(CoreModel):
    name: str
    access_key: Optional[str]


class UserInDB(IDModelMixin, UserBase):
    name: str


class UserPublic(IDModelMixin, UserBase):
    pass
