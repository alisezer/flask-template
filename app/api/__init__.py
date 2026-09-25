"""JSON API blueprint, mounted at /api/v1. HTTP errors are rendered as JSON by `app.errors`."""

from typing import Any

from flask import Blueprint, Response, jsonify
from pydantic import ValidationError

api = Blueprint("api", __name__)


@api.errorhandler(ValidationError)
def handle_validation_error(error: ValidationError) -> tuple[Response, int]:
    details: list[dict[str, Any]] = [
        {"field": ".".join(str(p) for p in err["loc"]), "message": err["msg"]}
        for err in error.errors(include_url=False)
    ]
    return jsonify(error="validation_error", details=details), 422


from app.api import stories  # noqa: E402, F401  (registers routes)
