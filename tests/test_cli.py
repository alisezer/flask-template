from flask import Flask

from app.extensions import db
from app.models import Story


def test_seed_creates_stories(app: Flask) -> None:
    result = app.test_cli_runner().invoke(args=["seed", "--count", "3"])

    assert result.exit_code == 0
    assert db.session.scalar(db.select(db.func.count(Story.id))) == 3
