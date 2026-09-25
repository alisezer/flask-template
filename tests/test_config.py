import pytest
from pydantic import ValidationError

from app.config import Settings


def test_production_requires_secret_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("SECRET_KEY", raising=False)

    with pytest.raises(ValidationError, match="SECRET_KEY must be set"):
        Settings(_env_file=None, APP_ENV="production")


def test_production_rejects_example_secret_key() -> None:
    with pytest.raises(ValidationError, match="SECRET_KEY must be set"):
        Settings(_env_file=None, APP_ENV="production", SECRET_KEY="change-me")


def test_production_config_is_hardened() -> None:
    config = Settings(_env_file=None, APP_ENV="production", SECRET_KEY="s3cret").flask_config()

    assert config["SESSION_COOKIE_SECURE"] is True
    assert config["WTF_CSRF_ENABLED"] is True
    assert config["TESTING"] is False


@pytest.mark.parametrize(
    "url",
    ["postgres://u:p@db:5432/stories", "postgresql://u:p@db:5432/stories"],
)
def test_postgres_urls_get_psycopg_driver(url: str) -> None:
    settings = Settings(_env_file=None, DATABASE_URL=url)

    assert settings.sqlalchemy_url == "postgresql+psycopg://u:p@db:5432/stories"


def test_secure_cookie_can_be_disabled_for_plain_http() -> None:
    settings = Settings(
        _env_file=None, APP_ENV="production", SECRET_KEY="s3cret", SESSION_COOKIE_SECURE=False
    )

    assert settings.flask_config()["SESSION_COOKIE_SECURE"] is False
