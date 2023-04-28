from pydantic import BaseModel


class CoreModel(BaseModel):
    pass


class IDModelMixin(BaseModel):
    """
    Миксин для добавления в модель поля id
    """
    id: int


class BaseResponse(BaseModel):
    """
    Базовая модель ответа должна содержать поле result
    """
    result: bool
