import os

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    PROJECT_NAME: str = "hirey"
    VERSION: str = "0.1.0"
    API_PREFIX: str = "/api"

    SECRET_KEY: SecretStr

    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_SERVER: str
    POSTGRES_PORT: str
    POSTGRES_DB: str

    DATABASE_URL: str = Field(
        description="The URL of Postgresdb",
        default=f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}",
    )


settings = Settings()
