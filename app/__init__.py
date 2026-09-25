"""Application factory.

`flask --app app ...` and `gunicorn "app:create_app()"` both find `create_app` here.
"""

from typing import Any

import click
from flask import Flask
from flask_migrate import upgrade
from sqlalchemy import text
from werkzeug.middleware.proxy_fix import ProxyFix

from app.config import Settings
from app.errors import register_error_handlers
from app.extensions import csrf, db, migrate
from app.logging import configure_logging


def create_app(overrides: dict[str, Any] | None = None) -> Flask:
    """Build the app. `overrides` are settings (e.g. `{"APP_ENV": "testing"}`) used by tests."""
    settings = Settings(**(overrides or {}))
    configure_logging(settings.LOG_LEVEL.upper())

    app = Flask(__name__)
    app.config.from_mapping(settings.flask_config())
    # Trust X-Forwarded-* headers from the single reverse proxy (nginx) in front of us.
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)  # type: ignore[method-assign]

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    from app.api import api
    from app.main import main

    app.register_blueprint(main)
    app.register_blueprint(api, url_prefix="/api/v1")

    register_error_handlers(app)
    register_health_check(app)
    register_commands(app)
    return app


def register_health_check(app: Flask) -> None:
    @app.get("/healthz")
    def healthz() -> tuple[dict[str, str], int]:
        try:
            db.session.execute(text("SELECT 1"))
        except Exception:
            app.logger.exception("Health check failed")
            return {"status": "error", "database": "unreachable"}, 503
        return {"status": "ok"}, 200


def register_commands(app: Flask) -> None:
    @app.cli.command()
    def deploy() -> None:
        """Run deployment tasks (apply database migrations)."""
        upgrade()

    @app.cli.command()
    @click.option("--count", default=5, show_default=True, help="Number of stories to create.")
    def seed(count: int) -> None:
        """Fill the database with sample stories."""
        from app.models import Story

        db.session.add_all(
            Story(
                title=f"Sample story {i}",
                topic="Examples",
                author="Flask Template",
                text=f"This is sample story number {i}. Edit or delete it from the web UI.",
            )
            for i in range(1, count + 1)
        )
        db.session.commit()
        click.echo(f"Created {count} stories.")
