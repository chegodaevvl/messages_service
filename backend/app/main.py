from fastapi import FastAPI

from app.core.settings import settings
from app.routes import router as api_router


def create_app() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    app.include_router(api_router, prefix=settings.API_PREFIX)
    return app


app = create_app()
