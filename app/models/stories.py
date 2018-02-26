"""This is an example model which will be used for creating stories on the web.
The model is defined in a similar way to python class/object, however is
inherited from a SQLAlchemy class so a DB entry with a table can be built
easily
"""

from datetime import datetime
from app import db


class Story(db.Model):
    # Table name which is going to store the stories defined here
    __tablename__ = 'stories'

    # These are the entries that are going to become columns in that table

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Story
    title = db.Column(db.String(255))
    topic = db.Column(db.String(255))
    text = db.Column(db.Text())
    author = db.Column(db.String(255))
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)

    def __init__(self, **kwargs):
        # Helps with class initiation, basically what every attribute you give
        # at initiaion will become a class attribute with this __init__ method
        super(Story, self).__init__(**kwargs)

    # The to json methods will be used for responding to API queries which are
    # going to be requesting story information.

    def to_full_json(self):
        json_story = {
            'id': self.id,
            'title': self.title,
            'topic': self.topic,
            'text': self.text,
            'author': self.author,
            'created_at': self.created_at,
        }
        return json_story

    def to_half_json(self):
        json_story = {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'created_at': self.created_at,
        }
        return json_story

    # This from json method is used for creating a story from a JSON.
    @staticmethod
    def from_json(json_post):
        title = json_post.get('title')
        topic = json_post.get('topic')
        text = json_post.get('text')
        author = json_post.get('author')

        story = Story(
            title=title,
            topic=topic,
            text=text,
            author=author
        )
        return story
