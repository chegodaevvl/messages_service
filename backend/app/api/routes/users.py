from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, Request
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN

from app.models.users import UserBase, UserPublic
from app.db.repositories.users import UserRepository
from app.api.dependencies.database import get_repository

router = APIRouter()


@router.get("/{id}/", response_model=UserPublic, name="users:get-user-by-id", status_code=HTTP_200_OK)
async def get_user_by_id(
        id: int,
        users_repo: UserRepository = Depends(get_repository(UserRepository)),
) -> UserPublic:
    user = await users_repo.get_user_by_id(id=id)

    if not user:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No user found with such id!")

    return user


@router.get("/me", response_model=UserPublic, name="users:get-user-by-secret", status_code=HTTP_200_OK)
async def get_user_by_id(
        request: Request,
        users_repo: UserRepository = Depends(get_repository(UserRepository)),
) -> UserPublic:
    secret = request.secret
    user = await users_repo.get_user_by_secret(secret=secret)

    if not user:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="You are not authorize yet")

    return user
