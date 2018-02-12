from app import db
import logging


# Logger Setup
logger = logging.getLogger(__name__)


class Example(db.Model):
    __tablename__ = 'examples'

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255), unique=True)

    registered = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow)

    def __init__(self, **kwargs):
        super(Bot, self).__init__(**kwargs)

    def save_example(self):
        db.session.add(self)
        db.session.commit()
