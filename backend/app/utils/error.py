from app.models.error import ErrorResponse


errors = {403: {"error_type": "Permission denied",
                "error_message": "You're not authorized!"},
          404: {"error_type": "Not Found",
                "error_message": "No user found with such id!"}}


async def create_error_response(error_code: int) -> ErrorResponse:
    return ErrorResponse(**{"result": False,
                            "error_type": errors[error_code]["error_type"],
                            "error_message": errors[error_code]["error_message"]})
