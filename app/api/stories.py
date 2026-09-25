"""CRUD endpoints for stories."""

from typing import Any

from flask import Response, current_app, jsonify, request, url_for
from werkzeug.exceptions import BadRequest, UnprocessableEntity

from app.api import api
from app.api.schemas import (
    PageParams,
    StoryCreate,
    StoryDetail,
    StoryList,
    StorySummary,
    StoryUpdate,
)
from app.extensions import csrf, db
from app.models import Story

# The API is stateless JSON (no cookies/sessions), so CSRF protection does not apply.
csrf.exempt(api)


def json_body() -> dict[str, Any]:
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        raise BadRequest("Request body must be a JSON object.")
    return data


def detail(story: Story) -> dict[str, Any]:
    return StoryDetail.model_validate(story).model_dump(mode="json")


@api.get("/stories/")
def list_stories() -> Response:
    params = PageParams.model_validate(request.args.to_dict())
    per_page = min(params.per_page, current_app.config["API_MAX_PER_PAGE"])
    pagination = db.paginate(
        db.select(Story).order_by(Story.created_at.desc(), Story.id.desc()),
        page=params.page,
        per_page=per_page,
        error_out=False,
    )
    body = StoryList(
        stories=[StorySummary.model_validate(s) for s in pagination.items],
        meta={
            "page": pagination.page,
            "per_page": pagination.per_page,
            "total": pagination.total or 0,
            "pages": pagination.pages,
        },
    )
    return jsonify(body.model_dump(mode="json"))


@api.get("/stories/<int:story_id>")
def get_story(story_id: int) -> Response:
    return jsonify(detail(db.get_or_404(Story, story_id)))


@api.post("/stories/")
def create_story() -> tuple[Response, int, dict[str, str]]:
    data = StoryCreate.model_validate(json_body())
    story = Story(**data.model_dump())
    db.session.add(story)
    db.session.commit()
    current_app.logger.info("Created story %s", story.id)
    location = url_for("api.get_story", story_id=story.id)
    return jsonify(detail(story)), 201, {"Location": location}


@api.put("/stories/<int:story_id>")
def replace_story(story_id: int) -> Response:
    story = db.get_or_404(Story, story_id)
    data = StoryCreate.model_validate(json_body())
    for field, value in data.model_dump().items():
        setattr(story, field, value)
    db.session.commit()
    current_app.logger.info("Replaced story %s", story.id)
    return jsonify(detail(story))


@api.patch("/stories/<int:story_id>")
def update_story(story_id: int) -> Response:
    story = db.get_or_404(Story, story_id)
    data = StoryUpdate.model_validate(json_body())
    for field, value in data.model_dump(exclude_unset=True).items():
        if value is None:
            raise UnprocessableEntity(f"'{field}' cannot be null.")
        setattr(story, field, value)
    db.session.commit()
    current_app.logger.info("Updated story %s", story.id)
    return jsonify(detail(story))


@api.delete("/stories/<int:story_id>")
def delete_story(story_id: int) -> tuple[str, int]:
    story = db.get_or_404(Story, story_id)
    db.session.delete(story)
    db.session.commit()
    current_app.logger.info("Deleted story %s", story_id)
    return "", 204
