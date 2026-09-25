"""Application settings, read from environment variables (and a local `.env` file).

Every setting can be overridden with an environment variable of the same name, e.g.
`DATABASE_URL=postgresql+psycopg://...`. See `.env.example` for the full list.
"""

from enum import StrEnum
from typing import Any, Self

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

INSECURE_SECRET_KEY = "dev-only-insecure-secret-key"  # noqa: S105
# Placeholder values that must never reach production.
PLACEHOLDER_SECRET_KEYS = {INSECURE_SECRET_KEY, "change-me", ""}


class Environment(StrEnum):
    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_ENV: Environment = Environment.DEVELOPMENT
    SECRET_KEY: str = INSECURE_SECRET_KEY
    DATABASE_URL: str = "sqlite:///stories.db"
    LOG_LEVEL: str = "INFO"
    STORIES_PER_PAGE: int = 10
    API_MAX_PER_PAGE: int = 100
    # Defaults to on in production. Turn off only when serving over plain HTTP.
    SESSION_COOKIE_SECURE: bool | None = None

    @model_validator(mode="after")
    def _check_production(self) -> Self:
        if self.APP_ENV is Environment.PRODUCTION and self.SECRET_KEY in PLACEHOLDER_SECRET_KEYS:
            raise ValueError("SECRET_KEY must be set in production")
        return self

    @property
    def sqlalchemy_url(self) -> str:
        # Hosting providers commonly hand out `postgres://` URLs; SQLAlchemy needs a driver.
        url = self.DATABASE_URL
        for prefix in ("postgres://", "postgresql://"):
            if url.startswith(prefix):
                return "postgresql+psycopg://" + url.removeprefix(prefix)
        return url

    def flask_config(self) -> dict[str, Any]:
        """Translate settings into the keys Flask and its extensions expect."""
        production = self.APP_ENV is Environment.PRODUCTION
        return {
            "APP_ENV": self.APP_ENV,
            "SECRET_KEY": self.SECRET_KEY,
            "SQLALCHEMY_DATABASE_URI": self.sqlalchemy_url,
            "SQLALCHEMY_ENGINE_OPTIONS": {"pool_pre_ping": True},
            "LOG_LEVEL": self.LOG_LEVEL.upper(),
            "STORIES_PER_PAGE": self.STORIES_PER_PAGE,
            "API_MAX_PER_PAGE": self.API_MAX_PER_PAGE,
            "TESTING": self.APP_ENV is Environment.TESTING,
            "WTF_CSRF_ENABLED": self.APP_ENV is not Environment.TESTING,
            "SESSION_COOKIE_SECURE": (
                production if self.SESSION_COOKIE_SECURE is None else self.SESSION_COOKIE_SECURE
            ),
            "SESSION_COOKIE_HTTPONLY": True,
            "SESSION_COOKIE_SAMESITE": "Lax",
        }
