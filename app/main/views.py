"""Server-rendered HTML pages."""

from flask import current_app, flash, redirect, render_template, request, url_for
from werkzeug.wrappers import Response

from app.extensions import db
from app.main import main
from app.main.forms import DeleteForm, StoryForm
from app.models import Story


@main.get("/")
def index() -> str:
    page = request.args.get("page", 1, type=int)
    pagination = db.paginate(
        db.select(Story).order_by(Story.created_at.desc(), Story.id.desc()),
        page=page,
        per_page=current_app.config["STORIES_PER_PAGE"],
    )
    return render_template("index.html", pagination=pagination)


@main.get("/stories/<int:story_id>")
def story(story_id: int) -> str:
    return render_template(
        "story.html", story=db.get_or_404(Story, story_id), delete_form=DeleteForm()
    )


@main.route("/stories/new", methods=["GET", "POST"])
def create_story() -> str | Response:
    form = StoryForm()
    if form.validate_on_submit():
        story = Story()
        form.populate_obj(story)
        db.session.add(story)
        db.session.commit()
        flash("Story created.", "success")
        return redirect(url_for("main.story", story_id=story.id))
    return render_template("edit_story.html", form=form, heading="New story")


@main.route("/stories/<int:story_id>/edit", methods=["GET", "POST"])
def edit_story(story_id: int) -> str | Response:
    story = db.get_or_404(Story, story_id)
    form = StoryForm(obj=story)
    if form.validate_on_submit():
        form.populate_obj(story)
        db.session.commit()
        flash("Story updated.", "success")
        return redirect(url_for("main.story", story_id=story.id))
    return render_template("edit_story.html", form=form, heading="Edit story", story=story)


@main.post("/stories/<int:story_id>/delete")
def delete_story(story_id: int) -> Response:
    story = db.get_or_404(Story, story_id)
    if DeleteForm().validate_on_submit():
        db.session.delete(story)
        db.session.commit()
        flash("Story deleted.", "success")
    return redirect(url_for("main.index"))
