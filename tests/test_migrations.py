"""Migrations must build the same schema as the models, from scratch and from old data."""

import sqlalchemy as sa
from flask_migrate import check, downgrade, upgrade

from app.extensions import db


def test_migrations_match_models(make_app) -> None:
    with make_app().app_context():
        upgrade()
        check()  # raises if autogenerate would produce a new migration


def test_upgrade_backfills_legacy_rows(make_app) -> None:
    with make_app().app_context():
        upgrade(revision="7b65bb46a819")
        db.session.execute(sa.text("INSERT INTO stories (title) VALUES ('legacy')"))
        db.session.commit()

        upgrade()
        row = db.session.execute(sa.text("SELECT * FROM stories")).mappings().one()

        assert row["title"] == "legacy"
        assert row["author"] == ""
        assert row["created_at"] is not None
        assert row["updated_at"] == row["created_at"]

        downgrade(revision="base")
