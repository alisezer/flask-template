"""HTML blueprint: the server-rendered web pages."""

from flask import Blueprint

main = Blueprint("main", __name__)

from app.main import views  # noqa: E402, F401  (registers routes)
