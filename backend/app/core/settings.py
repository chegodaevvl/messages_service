from os import path
from sys import modules

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    PROJECT_NAME: str = "TweetCo"
    PROJECT_VERSION: str = "0.0.1"
    API_PREFIX: str = "/api"
    SECRET_KEY: str = Field(default="Changeme")
    POSTGRES_USER: str = Field(default="Changeme")
    POSTGRES_PASSWORD: str = Field(default="Changeme")
    POSTGRES_SERVER: str = Field(default="Changeme")
    POSTGRES_PORT: str = Field(default="5432")
    POSTGRES_DB: str = Field(default="Changeme")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:"
            f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def MEDIA_PATH(self) -> str:
        if "pytest" in modules:
            return path.join("tests", "img")
        return "img"


settings = Settings()
