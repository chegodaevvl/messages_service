from fastapi import FastAPI

from settings import PROJECT_NAME, PROJECT_VERSION
from app.core.handlers import app_stop_app_handler, app_start_app_handler


def start_app() -> FastAPI:

    app = FastAPI(title=PROJECT_NAME, version=PROJECT_VERSION)

    app.add_event_handler("startup", app_start_app_handler(app))
    app.add_event_handler("shutdown", app_stop_app_handler(app))

    return app


app = start_app()
