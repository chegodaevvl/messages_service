from fastapi import Depends, FastAPI
from fastapi.staticfiles import StaticFiles

from app.core.settings import settings
from app.routes import router as api_router
from app.utils.authenticate import is_authenticate


def create_app() -> FastAPI:
    """
    Фабрика создания приложения FastAPI
    :return: приложение FastAPI
    """
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    app.include_router(
        api_router, prefix=settings.API_PREFIX, dependencies=[Depends(is_authenticate)]
    )
    app.mount(
        f"/{settings.MEDIA_PATH}",
        StaticFiles(directory=settings.MEDIA_PATH),
        name="images",
    )
    return app


app = create_app()
