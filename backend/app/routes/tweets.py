# from typing import Annotated
from fastapi import APIRouter, Depends, Header, Request
from fastapi import status

from app.db.repositories.users import UserCRUD
from app.db.repositories.tweets import TweetCRUD
from app.db.dependencies import get_user_crud, get_tweet_crud
from app.models.response import TweetResponse
from app.utils.error import create_error_response


router = APIRouter()


user_crud = Depends(get_user_crud)
tweet_crud = Depends(get_tweet_crud)


@router.post("", response_model=TweetResponse,
             response_model_exclude_unset=True,
             name="tweets:create-tweet",
             status_code=status.HTTP_200_OK)
async def create_tweet(
        request: Request,
        api_key: str = Header(default=None),
        user_crud: UserCRUD = user_crud,
        tweet_crud: TweetCRUD = tweet_crud,
) -> TweetResponse:
    user = await user_crud.get_by_apikey(api_key)
    tweet_data = await request.json()
    new_tweet = {
        "tweet_data": tweet_data["tweet_data"],
        "user_id": user.id
    }
    tweet_created = await tweet_crud.add_tweet(new_tweet)
    return {
        "result": True,
        "tweet_id": tweet_created.id,
    }


@router.delete("/{id}", response_model=TweetResponse,
               response_model_exclude_unset=True,
               name="tweets:delete-tweet",
               status_code=status.HTTP_200_OK)
async def delete_tweet(
        id: int,
        api_key: str = Header(default=None),
        user_crud: UserCRUD = user_crud,
        tweet_crud: TweetCRUD = tweet_crud,
) -> TweetResponse:
    user = await user_crud.get_by_apikey(api_key)
    if not await tweet_crud.check_by_id(id):
        return await create_error_response(104)
    if not await tweet_crud.check_ownership(id, user.id):
        return await create_error_response(105)
    result = await tweet_crud.delete_tweet(id)
    return {
        "result": result
    }


@router.post("/{id}/likes", response_model=TweetResponse,
             response_model_exclude_unset=True,
             name="tweets:like-tweet",
             status_code=status.HTTP_200_OK)
async def like_tweet(
        id: int,
        api_key: str = Header(default=None),
        user_crud: UserCRUD = user_crud,
        tweet_crud: TweetCRUD = tweet_crud,
) -> TweetResponse:
    user = await user_crud.get_by_apikey(api_key)
    if not await tweet_crud.check_by_id(id):
        return await create_error_response(104)
    if await tweet_crud.check_ownership(id, user.id):
        return await create_error_response(106)
    tweet_like = {
        "tweet_id": id,
        "user_id": user.id,
    }
    result = await tweet_crud.like_tweet(tweet_like)
    return {
        "result": result
    }


@router.delete("/{id}/likes", response_model=TweetResponse,
               response_model_exclude_unset=True,
               name="tweets:unlike-tweet",
               status_code=status.HTTP_200_OK)
async def unlike_tweet(
        id: int,
        api_key: str = Header(default=None),
        user_crud: UserCRUD = user_crud,
        tweet_crud: TweetCRUD = tweet_crud,
) -> TweetResponse:
    user = await user_crud.get_by_apikey(api_key)
    if not await tweet_crud.check_by_id(id):
        return await create_error_response(104)
    if await tweet_crud.check_ownership(id, user.id):
        return await create_error_response(106)
    if not await tweet_crud.check_tweet_like(id, user.id):
        return await create_error_response(107)
    tweet_like = {
        "tweet_id": id,
        "user_id": user.id,
    }
    result = await tweet_crud.unlike_tweet(tweet_like)
    return {
        "result": result
    }
