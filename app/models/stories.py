from datetime import datetime
from app import db
import logging


# Logger Setup
logger = logging.getLogger(__name__)


class Story(db.Model):
    __tablename__ = 'stories'

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Story
    title = db.Column(db.String(255))
    topic = db.Column(db.String(255))
    text = db.Column(db.Text())
    author = db.Column(db.String(255))
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)

    def __init__(self, **kwargs):
        super(Story, self).__init__(**kwargs)

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
