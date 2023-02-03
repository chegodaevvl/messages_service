from fastapi import APIRouter, Depends, Header
from fastapi import status

from app.db.repositories.users import UserCRUD
from app.db.dependencies import get_user_crud
from app.models.response import UserResponse
from app.models.error import ErrorResponse
from app.utils.error import create_error_response
from app.utils.authenticate import is_authenticate


router = APIRouter()


user_crud = Depends(get_user_crud)


@router.get("/me", name="users:get-current-user", status_code=status.HTTP_200_OK)
async def get_current_user(
        x_token: str = Header(default=None),
        user_crud: UserCRUD = user_crud,
):
    if not await is_authenticate(x_token, user_crud):
        return await create_error_response(403)
    user = await user_crud.get_by_apikey(x_token)
    return {
        "result": True,
        "user": user
    }


@router.get("/{id}", name="users:get-user-by-id", status_code=status.HTTP_200_OK)
async def get_user_by_id(
        id: int,
        x_token: str = Header(default=None),
        user_crud: UserCRUD = user_crud,
):
    if not await is_authenticate(x_token, user_crud):
        return await create_error_response(403)
    user = await user_crud.get_by_id(id)
    if not user:
        return await create_error_response(404)
    return {
        "result": True,
        "user": user
    }
