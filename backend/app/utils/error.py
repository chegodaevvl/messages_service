from app.models.error import ErrorResponse


errors = {
    101: {"error_type": "Not Found",
          "error_message": "No user found with such id!"},
    102: {"error_type": "Bad Request",
          "error_message": "You couldn't follow yourself!"},
    103: {"error_type": "Bad Request",
          "error_message": "You already follow this user!"},
}


async def create_error_response(error_code: int) -> ErrorResponse:
    return ErrorResponse(**{"result": False,
                            "error_type": errors[error_code]["error_type"],
                            "error_message": errors[error_code]["error_message"]})
