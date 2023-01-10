from fastapi import APIRouter, Depends
from fastapi import status

from app.models.response import UserResponse
from app.db.repositories.users import UserRepository
from app.api.dependencies.database import get_repository

router = APIRouter()


@router.get("/{id}", response_model=UserResponse, name="users:get-user-by-id", status_code=status.HTTP_200_OK)
async def get_user_by_id(
        id: int,
        users_repo: UserRepository = Depends(get_repository(UserRepository)),
) -> UserResponse:
    user = await users_repo.get_user_by_id(id=id)
    response = dict()
    if not user:
        response["result"] = False
        response["error_type"] = "Not Found"
        response["error_message"] = "No user found with such id!"
    else:
        response["result"] = True
        response["user"] = user

    return response


@router.get("/me", response_model=UserResponse, name="users:get-current-user", status_code=status.HTTP_200_OK)
async def get_current_user(
        secret: str,
        users_repo: UserRepository = Depends(get_repository(UserRepository)),
) -> UserResponse:
    user = await users_repo.get_user_by_secret(secret=secret)
    response = dict()
    if not user:
        response["result"] = False
        response["error_type"] = "Permission denied"
        response["error_message"] = "You're not authorized!"
    else:
        response["result"] = True
        response["user"] = user

    return response
