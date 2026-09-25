"""Web forms."""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


def strip(value: str | None) -> str | None:
    return value.strip() if isinstance(value, str) else value


class StoryForm(FlaskForm):  # type: ignore[misc]
    title = StringField("Title", validators=[DataRequired(), Length(max=255)], filters=[strip])
    topic = StringField("Topic", validators=[DataRequired(), Length(max=255)], filters=[strip])
    author = StringField("Author", validators=[DataRequired(), Length(max=255)], filters=[strip])
    text = TextAreaField("Story", validators=[DataRequired()], filters=[strip])
    submit = SubmitField("Save")


class DeleteForm(FlaskForm):  # type: ignore[misc]
    """Empty form: exists only to carry the CSRF token for delete buttons."""

    submit = SubmitField("Delete")
