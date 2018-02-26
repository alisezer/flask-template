"""Create a form for creating stories"""

from wtforms.validators import DataRequired, Length
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    SubmitField,
)

standard_validators = [DataRequired(), Length(0, 255)]


class StoryForm(FlaskForm):
    title = StringField('Title', validators=standard_validators)
    topic = StringField('Topic', validators=standard_validators)
    text = TextAreaField('Story', validators=[DataRequired()])
    author = StringField('Author', validators=standard_validators)
    submit = SubmitField('Submit')
