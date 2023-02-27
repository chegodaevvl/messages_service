from app.models.core import BaseResponse


class ErrorResponse(BaseResponse):
    error_type: str
    error_message: str

