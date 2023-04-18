from fastapi import APIRouter

from app.routes.media import router as media_routers
from app.routes.tweets import router as tweets_routers
from app.routes.users import router as users_routers

router = APIRouter()

router.include_router(users_routers, prefix="/users", tags=["users"])
router.include_router(tweets_routers, prefix="/tweets", tags=["tweets"])
router.include_router(media_routers, prefix="/media", tags=["media"])
