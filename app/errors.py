"""App-wide error pages. API routes get JSON (see `app.api`); everything else gets HTML."""

from flask import Flask, jsonify, render_template, request
from flask.typing import ResponseReturnValue
from werkzeug.exceptions import HTTPException


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(HTTPException)
    def handle_http_error(error: HTTPException) -> ResponseReturnValue:
        code = error.code or 500
        # Unknown URLs under /api never reach the API blueprint's own handler.
        if request.path.startswith("/api/"):
            return jsonify(
                error=error.name.lower().replace(" ", "_"), message=error.description
            ), code
        return render_template("errors/error.html", error=error), code
