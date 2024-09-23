"""Settings for units package."""

from functools import lru_cache

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings for units package."""

    #API_KEY: SecretStr
    #DATABASE_URL: SecretStr
    SENTRY_DSN: SecretStr = SecretStr("")

    HOST_IP: str = "0.0.0.0"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


@lru_cache()
def get_settings():
    """Returns settings object."""
    return Settings()
