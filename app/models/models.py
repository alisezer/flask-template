from datetime import datetime
from app import db
import logging


# Logger Setup
logger = logging.getLogger(__name__)


class Example(db.Model):
    __tablename__ = 'examples'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(255), unique=True)
    explanation = db.Column(db.String(255), unique=True)
    is_active = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow)

    def __init__(self, **kwargs):
        super(Example, self).__init__(**kwargs)

    def save_example(self):
        db.session.add(self)
        db.session.commit()

    def to_json(self):
        json_example = {
            'id': self.id,
            'name': self.name,
            'explanation': self.explanation,
            'is_active': self.is_active,
            'created_at': self.created_at,
            'updated_at': self.last_run_at,
        }
        return json_example
