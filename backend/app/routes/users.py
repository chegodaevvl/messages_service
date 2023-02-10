from fastapi import APIRouter, Depends, Header
from fastapi import status

from app.db.repositories.users import UserCRUD
from app.db.dependencies import get_user_crud
from app.models.response import UserResponse
from app.utils.error import create_error_response


router = APIRouter()


user_crud = Depends(get_user_crud)


@router.get("/me", response_model=UserResponse,
            response_model_exclude_unset=True,
            name="users:get-current-user",
            status_code=status.HTTP_200_OK)
async def get_current_user(
        x_token: str = Header(default=None),
        user_crud: UserCRUD = user_crud,
) -> UserResponse:
    user = await user_crud.get_by_apikey(x_token)
    return {
        "result": True,
        "user": user
    }


@router.get("/{id}", response_model=UserResponse,
            response_model_exclude_unset=True,
            name="users:get-user-by-id",
            status_code=status.HTTP_200_OK)
async def get_user_by_id(
        id: int,
        user_crud: UserCRUD = user_crud,
) -> UserResponse:
    user = await user_crud.get_by_id(id)
    if not user:
        return await create_error_response(404)
    return {
        "result": True,
        "user": user
    }


@router.post("/{id}/follow",
             response_model=UserResponse,
             response_model_exclude_unset=True,
             name="users:user_follow",
             status_code=status.HTTP_200_OK)
async def follow_user(
    id: int,
    x_token: str = Header(default=None),
    user_crud: UserCRUD = user_crud,
) -> UserResponse:
    print(id)
    print(x_token)
    following_user = await user_crud.get_by_apikey(x_token)
    print(following_user.id)
    followed_user = await user_crud.get_by_id(id)
    print(followed_user.id)
    if not followed_user:
        return await create_error_response(404)
    if following_user == followed_user:
        return await create_error_response(401)
    result = await user_crud.add_follower(followed_user.id, following_user.id)
    print(result)
    if not result:
        return await create_error_response(402)
    return {
        "result": True,
    }
