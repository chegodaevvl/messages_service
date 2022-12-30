from fastapi import FastAPI

from app.core.settings import settings
from app.core.handlers import app_stop_app_handler, app_start_app_handler
from app.api.routes import router as api_router


def start_app() -> FastAPI:

    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

    app.add_event_handler("startup", app_start_app_handler(app))
    app.add_event_handler("shutdown", app_stop_app_handler(app))

    app.include_router(api_router, prefix=settings.API_PREFIX)

    return app


app = start_app()
