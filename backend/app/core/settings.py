from pydantic import BaseSettings, Field, SecretStr


class Settings(BaseSettings):
    PROJECT_NAME: str = "TweetCo"
    PROJECT_VERSION: str = "0.0.1"
    API_PREFIX: str = "/api"
    SECRET_KEY: str = Field(default="Changeme")
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: str = Field(default='5432')
    POSTGRES_DB: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        # secrets_dir = "/secrets/"

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:" \
               f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:" \
               f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


settings = Settings()
