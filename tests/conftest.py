from collections.abc import Callable, Iterator
from pathlib import Path
from typing import Any

import pytest
from flask import Flask
from flask.testing import FlaskClient

from app import create_app
from app.extensions import db
from app.models import Story


@pytest.fixture
def make_app(tmp_path: Path) -> Iterator[Callable[..., Flask]]:
    """Build apps on a temporary SQLite file; their connections are closed afterwards."""
    apps: list[Flask] = []

    def _make(**overrides: Any) -> Flask:
        settings = {"APP_ENV": "testing", "DATABASE_URL": f"sqlite:///{tmp_path / 'test.db'}"}
        app = create_app(settings | overrides)
        apps.append(app)
        return app

    yield _make
    for app in apps:
        with app.app_context():
            db.engine.dispose()


@pytest.fixture
def app(make_app: Callable[..., Flask]) -> Iterator[Flask]:
    app = make_app()
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()


@pytest.fixture
def make_story(app: Flask):  # type: ignore[no-untyped-def]
    def _make(**overrides: str) -> Story:
        fields = {
            "title": "A title",
            "topic": "A topic",
            "text": "Once upon a time.",
            "author": "Ali",
        }
        story = Story(**(fields | overrides))
        db.session.add(story)
        db.session.commit()
        return story

    return _make
