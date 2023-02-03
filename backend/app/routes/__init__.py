from fastapi import APIRouter

from app.routes.users import router as users_routers


router = APIRouter()

router.include_router(users_routers, prefix="/users", tags=["users"])
