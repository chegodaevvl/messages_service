from databases import DatabaseURL
from starlette.config import Config
from starlette.datastructures import Secret


settings = Config(".env")

PROJECT_NAME = "TweetCo"
PROJECT_VERSION = "0.0.1"
API_PREFIX = "/api"

SECRET_KEY = settings("SECRET_KEY", cast=Secret, default="CHANGEME")

POSTGRES_USER = settings("POSTGRES_USER", cast=str)
POSTGRES_PASSWORD = settings("POSTGRES_PASSWORD", cast=Secret)
POSTGRES_SERVER = settings("POSTGRES_SERVER", cast=str, default="db_server")
POSTGRES_PORT = settings("POSTGRES_PORT", cast=str, default="5432")
POSTGRES_DB = settings("POSTGRES_DB", cast=str)

DATABASE_URL = settings(
    "DATABASE_URL",
    cast=DatabaseURL,
    default=f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
)
