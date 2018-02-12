from flask import jsonify, request, current_app, url_for
from app.api import api
from app.models.models import Example


@api.route('/examples/')
def get_examples():
    examples = Example.query.all()
    return jsonify({
        'examples': [Example.to_json() for example in examples]
    })
