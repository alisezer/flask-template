from flask import Flask
from flask.testing import FlaskClient

from app.extensions import db
from app.models import Story

FORM = {"title": "Web story", "topic": "Web", "text": "Typed in a browser.", "author": "Ali"}


def test_index_empty(client: FlaskClient) -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert b"No stories yet" in response.data


def test_index_lists_and_paginates(client: FlaskClient, app: Flask, make_story) -> None:
    app.config["STORIES_PER_PAGE"] = 2
    for i in range(3):
        make_story(title=f"Story number {i}")

    page1 = client.get("/").get_data(as_text=True)
    page2 = client.get("/?page=2").get_data(as_text=True)

    assert "Story number 2" in page1
    assert "Story number 0" not in page1
    assert "Story number 0" in page2


def test_story_page(client: FlaskClient, make_story) -> None:
    story = make_story(text="Line one\nLine two")

    response = client.get(f"/stories/{story.id}")

    assert response.status_code == 200
    assert b"Line one\nLine two" in response.data


def test_story_page_escapes_html(client: FlaskClient, make_story) -> None:
    story = make_story(title="<script>alert(1)</script>")

    assert b"<script>alert(1)" not in client.get(f"/stories/{story.id}").data


def test_missing_story_renders_html_404(client: FlaskClient) -> None:
    response = client.get("/stories/999")

    assert response.status_code == 404
    assert response.mimetype == "text/html"
    assert b"Not Found" in response.data


def test_create_story(client: FlaskClient) -> None:
    response = client.post("/stories/new", data=FORM)

    story = db.session.scalars(db.select(Story)).one()
    assert response.status_code == 302
    assert response.headers["Location"] == f"/stories/{story.id}"
    # Regression: the author used to be saved as the story text.
    assert story.author == "Ali"
    assert story.text == "Typed in a browser."


def test_create_story_shows_validation_errors(client: FlaskClient) -> None:
    response = client.post("/stories/new", data=FORM | {"title": "   "})

    assert response.status_code == 200
    assert b"is-invalid" in response.data
    assert db.session.scalars(db.select(Story)).first() is None


def test_edit_story(client: FlaskClient, make_story) -> None:
    story = make_story()

    form_page = client.get(f"/stories/{story.id}/edit")
    response = client.post(f"/stories/{story.id}/edit", data=FORM | {"title": "Edited"})

    assert b'value="A title"' in form_page.data
    assert response.status_code == 302
    assert db.session.get(Story, story.id).title == "Edited"


def test_delete_story(client: FlaskClient, make_story) -> None:
    story_id = make_story().id

    response = client.post(f"/stories/{story_id}/delete", follow_redirects=True)

    assert b"Story deleted." in response.data
    assert db.session.get(Story, story_id) is None


def test_forms_require_csrf_outside_tests(make_app) -> None:
    app = make_app(APP_ENV="development")
    with app.app_context():
        db.create_all()
        response = app.test_client().post("/stories/new", data=FORM)

    assert response.status_code == 400
    assert b"CSRF token is missing" in response.data
