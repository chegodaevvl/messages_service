from typing import Union

from fastapi import APIRouter, Depends, Header, status

from app.db.dependencies import get_user_crud
from app.db.repositories.users import UserCRUD
from app.models.error import ErrorResponse
from app.models.response import UserResponse
from app.models.users import FollowerInfo, UserPublic
from app.utils.error import create_error_response

router = APIRouter()


user_crud = Depends(get_user_crud)


@router.get(
    "/me",
    response_model=UserResponse,
    response_model_exclude_unset=True,
    name="users:get-current-user",
    status_code=status.HTTP_200_OK,
)
async def get_current_user(
    api_key: str = Header(default=None),
    user_crud: UserCRUD = user_crud,
) -> UserResponse:
    user = await user_crud.get_by_apikey(api_key)
    followers = await user_crud.get_followers(user.id)  # type: ignore
    followings = await user_crud.get_followings(user.id)  # type: ignore
    user_detail = UserPublic(
        id=user.id,  # type: ignore
        name=user.name,  # type: ignore
        followers=followers,  # type: ignore
        following=followings,  # type: ignore
    )
    return UserResponse(
        result=True, user=user_detail, error_type=None, error_message=None
    )


@router.get(
    "/{id}",
    response_model=UserResponse,
    response_model_exclude_unset=True,
    name="users:get-user-by-id",
    status_code=status.HTTP_200_OK,
)
async def get_user_by_id(
    id: int,
    user_crud: UserCRUD = user_crud,
) -> Union[UserResponse, ErrorResponse]:
    user = await user_crud.get_by_id(id)
    if not user:
        return await create_error_response(101)
    followers = await user_crud.get_followers(user.id)  # type: ignore
    followings = await user_crud.get_followings(user.id)  # type: ignore
    user_detail = UserPublic(
        id=user.id,  # type: ignore
        name=user.name,  # type: ignore
        followers=followers,
        following=followings,
    )
    return UserResponse(
        result=True, user=user_detail, error_type=None, error_message=None
    )


@router.post(
    "/{id}/follow",
    response_model=UserResponse,
    response_model_exclude_unset=True,
    name="users:user_follow",
    status_code=status.HTTP_200_OK,
)
async def follow_user(
    id: int,
    api_key: str = Header(default=None),
    user_crud: UserCRUD = user_crud,
) -> Union[UserResponse, ErrorResponse]:
    following_user = await user_crud.get_by_apikey(api_key)
    followed_user = await user_crud.get_by_id(id)
    if not followed_user:
        return await create_error_response(101)
    if following_user == followed_user:
        return await create_error_response(102)
    follower = FollowerInfo(
        following_id=followed_user.id, follower_id=following_user.id  # type: ignore
    )
    result = await user_crud.add_follower(follower)
    if not result:
        return await create_error_response(103)
    return UserResponse(result=True, user=None, error_type=None, error_message=None)


@router.delete(
    "/{id}/follow",
    response_model=UserResponse,
    response_model_exclude_unset=True,
    name="users:user_unfollow",
    status_code=status.HTTP_200_OK,
)
async def unfollow_user(
    id: int,
    api_key: str = Header(default=None),
    user_crud: UserCRUD = user_crud,
) -> Union[UserResponse, ErrorResponse]:
    following_user = await user_crud.get_by_apikey(api_key)
    followed_user = await user_crud.get_by_id(id)
    if not followed_user:
        return await create_error_response(101)
    if following_user == followed_user:
        return await create_error_response(102)
    follower = FollowerInfo(
        following_id=followed_user.id, follower_id=following_user.id  # type: ignore
    )
    result = await user_crud.remove_follower(follower)
    if not result:
        return await create_error_response(103)
    return UserResponse(result=True, user=None, error_type=None, error_message=None)
