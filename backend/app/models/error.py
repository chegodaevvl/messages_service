from app.models.core import BaseResponse


class ErrorResponse(BaseResponse):
    """
    Модель описания ответа с ошибкой
    """
    error_type: str
    error_message: str
