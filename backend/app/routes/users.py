# from typing import Annotated
from fastapi import APIRouter, Depends, Header
from fastapi import status

from app.db.repositories.users import UserCRUD
from app.db.dependencies import get_user_crud
from app.models.response import UserResponse
from app.models.users import FollowerInfo
from app.utils.error import create_error_response


router = APIRouter()


user_crud = Depends(get_user_crud)


@router.get("/me", response_model=UserResponse,
            response_model_exclude_unset=True,
            name="users:get-current-user",
            status_code=status.HTTP_200_OK)
async def get_current_user(
        api_key: str = Header(default=None),
        user_crud: UserCRUD = user_crud,
) -> UserResponse:
    user = await user_crud.get_by_apikey(api_key)
    user_detail = {
        "id": user.id,
        "name": user.name
    }
    followers = await user_crud.get_followers(user.id)
    followings = await user_crud.get_followings(user.id)
    if followers:
        user_detail["followers"] = followers
    if followings:
        user_detail["following"] = followings
    return {
        "result": True,
        "user": user_detail
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
        return await create_error_response(101)
    user_detail = {
        "id": user.id,
        "name": user.name
    }
    followers = await user_crud.get_followers(user.id)
    followings = await user_crud.get_followings(user.id)
    if followers:
        user_detail["followers"] = followers
    if followings:
        user_detail["following"] = followings
    return {
        "result": True,
        "user": user_detail
    }


@router.post("/{id}/follow",
             response_model=UserResponse,
             response_model_exclude_unset=True,
             name="users:user_follow",
             status_code=status.HTTP_200_OK)
async def follow_user(
    id: int,
    api_key: str = Header(default=None),
    user_crud: UserCRUD = user_crud,
) -> UserResponse:
    following_user = await user_crud.get_by_apikey(api_key)
    followed_user = await user_crud.get_by_id(id)
    if not followed_user:
        return await create_error_response(101)
    if following_user == followed_user:
        return await create_error_response(102)
    follower = FollowerInfo(
        following_id=followed_user.id,
        follower_id=following_user.id
    )
    result = await user_crud.add_follower(follower)
    if not result:
        return await create_error_response(103)
    return {
        "result": True,
    }


@router.delete("/{id}/follow",
               response_model=UserResponse,
               response_model_exclude_unset=True,
               name="users:user_unfollow",
               status_code=status.HTTP_200_OK)
async def unfollow_user(
    id: int,
    api_key: str = Header(default=None),
    user_crud: UserCRUD = user_crud,
) -> UserResponse:
    following_user = await user_crud.get_by_apikey(api_key)
    followed_user = await user_crud.get_by_id(id)
    if not followed_user:
        return await create_error_response(101)
    if following_user == followed_user:
        return await create_error_response(102)
    follower = FollowerInfo(
        following_id=followed_user.id,
        follower_id=following_user.id
    )
    result = await user_crud.remove_follower(follower)
    if not result:
        return await create_error_response(103)
    return {
        "result": True,
    }
