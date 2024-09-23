"""Settings for units package."""

from functools import lru_cache
from typing import Optional

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings for units package."""

    UNITS_SENTRY_DSN: Optional[SecretStr] = SecretStr("")
    UNITS_SPARQL_URL: Optional[str] = "https://fuseki.d-d-s.ch/skosmos/query"
    UNITS_VOCAB_PREFIX: Optional[str] = "https://vocab.sentier.dev/"
    UNITS_HOST_IP: str = "0.0.0.0"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


@lru_cache()
def get_settings():
    """Returns settings object."""
    return Settings()
