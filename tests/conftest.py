from collections.abc import Iterator
from pathlib import Path

import pytest
from flask import Flask
from flask.testing import FlaskClient

from app import create_app
from app.extensions import db
from app.models import Story


@pytest.fixture
def app(tmp_path: Path) -> Iterator[Flask]:
    app = create_app({"APP_ENV": "testing", "DATABASE_URL": f"sqlite:///{tmp_path / 'test.db'}"})
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
