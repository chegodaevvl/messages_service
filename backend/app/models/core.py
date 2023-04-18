from pydantic import BaseModel


class CoreModel(BaseModel):
    pass


class IDModelMixin(BaseModel):
    id: int


class BaseResponse(BaseModel):
    result: bool
