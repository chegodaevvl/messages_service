from app.models.error import ErrorResponse

errors = {
    101: {"error_type": "Not Found", "error_message": "No user found with such id!"},
    102: {
        "error_type": "Bad Request",
        "error_message": "It is unable to perform such operation on your own account!",
    },
    103: {
        "error_type": "Bad Request",
        "error_message": "You already follow this user!",
    },
    104: {"error_type": "Not Found", "error_message": "No tweet found with such id!"},
    105: {
        "error_type": "Not Authorized",
        "error_message": "You are unable to delete tweet, created by another user!",
    },
    106: {
        "error_type": "Bad Request",
        "error_message": "You are unable to like/unlike your own tweet!",
    },
    107: {
        "error_type": "Bad Request",
        "error_message": "You are unable to unlike tweet, you don't like!",
    },
    108: {
        "error_type": "Bad Request",
        "error_message": "Uploaded file is not an image!",
    },
    109: {
        "error_type": "Bad Request",
        "error_message": "Wrong number of the tweet images!",
    },
}


async def create_error_response(error_code: int) -> ErrorResponse:
    return ErrorResponse(
        **{
            "result": False,
            "error_type": errors[error_code]["error_type"],
            "error_message": errors[error_code]["error_message"],
        }
    )
