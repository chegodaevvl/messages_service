from typing import Optional
from pydantic import BaseModel


class CoreModel(BaseModel):
    pass


class IDModelMixin(BaseModel):
    id: int


class BaseResponse(BaseModel):
    result: bool
    error_type: Optional[str]
    error_message: Optional[str]
