from fastapi import APIRouter

from app.routes.users import router as users_routers
from app.routes.tweets import router as tweets_routers


router = APIRouter()

router.include_router(users_routers, prefix="/users", tags=["users"])
router.include_router(tweets_routers, prefix="/tweets", tags=["tweets"])
