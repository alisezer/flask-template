import pytest
from flask.testing import FlaskClient

from app.extensions import db
from app.models import Story

VALID = {"title": "The Title", "topic": "Fiction", "text": "It was a dark night.", "author": "Ali"}


def test_create_story(client: FlaskClient) -> None:
    response = client.post("/api/v1/stories/", json=VALID)

    assert response.status_code == 201
    body = response.get_json()
    assert body["id"] > 0
    assert {k: body[k] for k in VALID} == VALID
    assert response.headers["Location"] == f"/api/v1/stories/{body['id']}"
    assert db.session.get(Story, body["id"]) is not None


def test_create_strips_whitespace(client: FlaskClient) -> None:
    response = client.post("/api/v1/stories/", json=VALID | {"title": "  Padded  "})

    assert response.get_json()["title"] == "Padded"


@pytest.mark.parametrize(
    ("payload", "field"),
    [
        ({k: v for k, v in VALID.items() if k != "title"}, "title"),
        (VALID | {"author": ""}, "author"),
        (VALID | {"topic": "x" * 256}, "topic"),
        (VALID | {"text": 42}, "text"),
        (VALID | {"unknown": "field"}, "unknown"),
    ],
)
def test_create_rejects_invalid_payload(client: FlaskClient, payload: dict, field: str) -> None:
    response = client.post("/api/v1/stories/", json=payload)

    assert response.status_code == 422
    body = response.get_json()
    assert body["error"] == "validation_error"
    assert field in [d["field"] for d in body["details"]]


@pytest.mark.parametrize("body", ["not json", "[1, 2]"])
def test_create_rejects_non_object_body(client: FlaskClient, body: str) -> None:
    response = client.post("/api/v1/stories/", data=body, content_type="application/json")

    assert response.status_code == 400
    assert response.get_json()["error"] == "bad_request"


def test_get_story(client: FlaskClient, make_story) -> None:
    story = make_story()

    body = client.get(f"/api/v1/stories/{story.id}").get_json()

    assert body["id"] == story.id
    assert body["text"] == story.text
    assert body["created_at"].endswith("Z")
    assert body["updated_at"].endswith("Z")


def test_get_missing_story_returns_json_404(client: FlaskClient) -> None:
    response = client.get("/api/v1/stories/999")

    assert response.status_code == 404
    assert response.get_json()["error"] == "not_found"


def test_unknown_api_url_returns_json_404(client: FlaskClient) -> None:
    response = client.get("/api/v1/nope")

    assert response.status_code == 404
    assert response.is_json


def test_list_stories_newest_first_without_text(client: FlaskClient, make_story) -> None:
    first, second = make_story(title="first"), make_story(title="second")

    body = client.get("/api/v1/stories/").get_json()

    assert [s["id"] for s in body["stories"]] == [second.id, first.id]
    assert "text" not in body["stories"][0]
    assert body["meta"] == {"page": 1, "per_page": 20, "total": 2, "pages": 1}


def test_list_stories_paginates(client: FlaskClient, make_story) -> None:
    for i in range(5):
        make_story(title=f"story {i}")

    body = client.get("/api/v1/stories/?page=2&per_page=2").get_json()

    assert [s["title"] for s in body["stories"]] == ["story 2", "story 1"]
    assert body["meta"] == {"page": 2, "per_page": 2, "total": 5, "pages": 3}


def test_list_caps_per_page(client: FlaskClient, app) -> None:
    app.config["API_MAX_PER_PAGE"] = 3

    body = client.get("/api/v1/stories/?per_page=1000").get_json()

    assert body["meta"]["per_page"] == 3


@pytest.mark.parametrize("query", ["page=0", "per_page=-1", "page=abc"])
def test_list_rejects_bad_pagination(client: FlaskClient, query: str) -> None:
    assert client.get(f"/api/v1/stories/?{query}").status_code == 422


def test_replace_story(client: FlaskClient, make_story) -> None:
    story = make_story()
    new = VALID | {"title": "Replaced"}

    response = client.put(f"/api/v1/stories/{story.id}", json=new)

    assert response.status_code == 200
    assert db.session.get(Story, story.id).title == "Replaced"


def test_replace_requires_all_fields(client: FlaskClient, make_story) -> None:
    story = make_story()

    response = client.put(f"/api/v1/stories/{story.id}", json={"title": "Only title"})

    assert response.status_code == 422
    assert db.session.get(Story, story.id).title == "A title"


def test_patch_updates_only_sent_fields(client: FlaskClient, make_story) -> None:
    story = make_story()

    response = client.patch(f"/api/v1/stories/{story.id}", json={"title": "Patched"})

    assert response.status_code == 200
    body = response.get_json()
    assert body["title"] == "Patched"
    assert body["author"] == "Ali"


def test_patch_rejects_null(client: FlaskClient, make_story) -> None:
    story = make_story()

    response = client.patch(f"/api/v1/stories/{story.id}", json={"title": None})

    assert response.status_code == 422


def test_delete_story(client: FlaskClient, make_story) -> None:
    story = make_story()
    story_id = story.id

    assert client.delete(f"/api/v1/stories/{story_id}").status_code == 204
    assert client.get(f"/api/v1/stories/{story_id}").status_code == 404


def test_healthz(client: FlaskClient) -> None:
    assert client.get("/healthz").get_json() == {"status": "ok"}
