from flask import jsonify, request, current_app
from app.models.stories import Story
from app.api import api
from app import db


@api.route('/stories/', methods=['GET'])
def get_stories():
    current_app.logger.info('Retrieving all stories')
    current_app.logger.debug('Will you see this?')
    stories = Story.query.all()
    return jsonify({
        'stories': [story.to_half_json() for story in stories]
    })


@api.route('/stories/<int:id>', methods=['GET'])
def get_story(id):
    story = Story.query.get_or_404(id)
    current_app.logger.info('Retrieving story {}'.format(id))
    return jsonify(story.to_full_json())


@api.route('/stories/', methods=['POST'])
def new_story():
    story = Story.from_json(request.json)
    current_app.logger.info('Creating new story')
    db.session.add(story)
    db.session.commit()
    return jsonify(story.to_full_json()), 201


@api.route('/stories/<int:id>', methods=['PUT'])
def edit_story(id):
    story = Story.query.get_or_404(id)
    story.title = request.json.get('title')
    story.topic = request.json.get('topic')
    story.text = request.json.get('text')
    story.author = request.json.get('author')

    current_app.logger.info('Editing story {}'.format(id))
    db.session.add(story)
    db.session.commit()
    return jsonify(story.to_full_json())
