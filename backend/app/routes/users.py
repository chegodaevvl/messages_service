from fastapi import APIRouter, Depends, Header
from fastapi import status

from app.db.repositories.users import UserCRUD
from app.db.dependencies import get_user_crud
from app.models.response import UserResponse
from app.models.error import ErrorResponse
from app.utils.error import create_error_response


router = APIRouter()


user_crud = Depends(get_user_crud)


@router.get("/me", response_model=UserResponse, name="users:get-current-user", status_code=status.HTTP_200_OK)
async def get_current_user(
        x_token: str | None = Header(default=None),
        user_crud: UserCRUD = user_crud,
) -> UserResponse | ErrorResponse:
    if not x_token:
        return create_error_response(403)


# @router.get("/{id}", response_model=UserResponse, name="users:get-user-by-id", status_code=status.HTTP_200_OK)
# async def get_user_by_id(
#         id: int,
#         users_crud: UserCRUD = user_crud,
# ) -> UserResponse:
#     pass
