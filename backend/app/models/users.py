from typing import Optional
from app.models.core import CoreModel, IDModelMixin


class UserBase(CoreModel):
    name: str


class UserCreate(UserBase):
    name: str
    access_key: str


class UserInDB(IDModelMixin, UserBase):
    name: str
    access_key: Optional[str]


class UserPublic(IDModelMixin, UserBase):
    pass
