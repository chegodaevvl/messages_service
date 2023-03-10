from fastapi import APIRouter, Depends, Header, Request
from fastapi import status

from app.db.repositories.users import UserCRUD
from app.db.repositories.tweets import TweetCRUD
from app.db.dependencies import get_user_crud, get_tweet_crud
from app.models.response import TweetResponse


router = APIRouter()


user_crud = Depends(get_user_crud)
tweet_crud = Depends(get_tweet_crud)


@router.post("", response_model=TweetResponse,
             response_model_exclude_unset=True,
             name="tweets:create-tweet",
             status_code=status.HTTP_200_OK)
async def create_tweet(
        request: Request,
        x_token: str = Header(default=None),
        user_crud: UserCRUD = user_crud,
        tweet_crud: TweetCRUD = tweet_crud,
) -> TweetResponse:
    user = await user_crud.get_by_apikey(x_token)
    tweet_data = await request.json()
    new_tweet = {
        "tweet_data": tweet_data["tweet_data"],
        "user_id": user.id
    }
    tweet_created = await tweet_crud.add_tweet(new_tweet)
    print(tweet_created)
    return {
        "result": True,
        "tweet_id": tweet_created.id,
    }
