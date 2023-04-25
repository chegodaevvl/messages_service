from os import path, remove
from typing import Union

from fastapi import APIRouter, Depends, Header, Request, status

from app.core.settings import settings
from app.db.dependencies import get_media_crud, get_tweet_crud, get_user_crud
from app.db.repositories.media import MediaCRUD
from app.db.repositories.tweets import TweetCRUD
from app.db.repositories.users import UserCRUD
from app.models.response import TweetResponse, TweetsResponse
from app.models.error import ErrorResponse
from app.models.tweets import TweetCreate, TweetPublic, TweetLike
from app.utils.error import create_error_response

router = APIRouter()


user_crud = Depends(get_user_crud)
tweet_crud = Depends(get_tweet_crud)
media_crud = Depends(get_media_crud)


@router.post(
    "",
    response_model=TweetResponse,
    response_model_exclude_unset=True,
    name="tweets:create-tweet",
    status_code=status.HTTP_200_OK,
)
async def create_tweet(
    request: Request,
    api_key: str = Header(default=None),
    user_crud: UserCRUD = user_crud,
    tweet_crud: TweetCRUD = tweet_crud,
    media_crud: MediaCRUD = media_crud,
) -> Union[TweetResponse, ErrorResponse]:
    user = await user_crud.get_by_apikey(api_key)
    tweet_data = await request.json()
    # new_tweet = {"tweet_data": tweet_data["tweet_data"], "user_id": user.id}
    new_tweet = TweetCreate(
        tweet_data=tweet_data["tweet_data"],
        user_id=user.id                                                                 # type: ignore
    )
    images_ids = None
    if "tweet_media_ids" in tweet_data:
        images_ids = tweet_data["tweet_media_ids"]
        if not await media_crud.check_images_exist(images_ids):
            return await create_error_response(109)
    tweet_created = await tweet_crud.add_tweet(new_tweet)
    if images_ids:
        await media_crud.link_images_to_tweet(tweet_created.id, images_ids)
    return TweetResponse(
        result=True,
        tweet_id=tweet_created.id,
    )


@router.delete(
    "/{id}",
    response_model=TweetResponse,
    response_model_exclude_unset=True,
    name="tweets:delete-tweet",
    status_code=status.HTTP_200_OK,
)
async def delete_tweet(
    id: int,
    api_key: str = Header(default=None),
    user_crud: UserCRUD = user_crud,
    tweet_crud: TweetCRUD = tweet_crud,
    media_crud: MediaCRUD = media_crud,
) -> Union[TweetResponse, ErrorResponse]:
    user = await user_crud.get_by_apikey(api_key)
    if not await tweet_crud.check_by_id(id):
        return await create_error_response(104)
    if not await tweet_crud.check_ownership(id, user.id):                           # type: ignore
        return await create_error_response(105)
    images_list = await media_crud.get_images_by_tweet(id)
    result = await tweet_crud.delete_tweet(id)
    for image in images_list:
        remove(path.join(settings.MEDIA_PATH, image))
    return TweetResponse(
        result=result,
        tweet_id=0,
    )


@router.get(
    "",
    response_model=TweetsResponse,
    response_model_exclude_unset=True,
    name="tweets:get-tweets",
    status_code=status.HTTP_200_OK,
)
async def get_tweets(
    api_key: str = Header(default=None),
    user_crud: UserCRUD = user_crud,
    tweet_crud: TweetCRUD = tweet_crud,
) -> Union[TweetsResponse, ErrorResponse]:
    user = await user_crud.get_by_apikey(api_key)
    tweets_list = await tweet_crud.get_tweets(user.id)                          # type: ignore
    tweets = list()
    for tweet in tweets_list:
        attachments = list()
        for attachment in tweet.media:
            attachments.append(attachment.link)
        likes = list()
        for like in tweet.likes:
            likes.append(like.liker)
        tweet_details = TweetPublic(
            id=tweet.id,                                                        # type: ignore
            content=tweet.tweet_data,                                           # type: ignore
            attachments=attachments,
            author=tweet.author,
            likes=likes,
        )
        tweets.append(tweet_details)
    return TweetsResponse(
        result=True,
        tweets=tweets
    )


@router.post(
    "/{id}/likes",
    response_model=TweetResponse,
    response_model_exclude_unset=True,
    name="tweets:like-tweet",
    status_code=status.HTTP_200_OK,
)
async def like_tweet(
    id: int,
    api_key: str = Header(default=None),
    user_crud: UserCRUD = user_crud,
    tweet_crud: TweetCRUD = tweet_crud,
) -> Union[TweetResponse, ErrorResponse]:
    user = await user_crud.get_by_apikey(api_key)
    if not await tweet_crud.check_by_id(id):
        return await create_error_response(104)
    if await tweet_crud.check_ownership(id, user.id):                       # type: ignore
        return await create_error_response(106)
    tweet_like = TweetLike(
        tweet_id=id,
        user_id=user.id,                                                    # type: ignore
    )
    result = await tweet_crud.like_tweet(tweet_like)
    return TweetResponse(
        result=result,
        tweet_id=None
    )


@router.delete(
    "/{id}/likes",
    response_model=TweetResponse,
    response_model_exclude_unset=True,
    name="tweets:unlike-tweet",
    status_code=status.HTTP_200_OK,
)
async def unlike_tweet(
    id: int,
    api_key: str = Header(default=None),
    user_crud: UserCRUD = user_crud,
    tweet_crud: TweetCRUD = tweet_crud,
) -> Union[TweetResponse, ErrorResponse]:
    user = await user_crud.get_by_apikey(api_key)
    if not await tweet_crud.check_by_id(id):
        return await create_error_response(104)
    if await tweet_crud.check_ownership(id, user.id):                               # type: ignore
        return await create_error_response(106)
    if not await tweet_crud.check_tweet_like(id, user.id):                          # type: ignore
        return await create_error_response(107)
    tweet_like = TweetLike(
        tweet_id=id,
        user_id=user.id,                                                            # type: ignore
    )
    result = await tweet_crud.unlike_tweet(tweet_like)
    return TweetResponse(
        result=result,
        tweet_id=None,
    )
