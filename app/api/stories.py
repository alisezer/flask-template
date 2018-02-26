"""Registers the necessary routes for the story model."""

from flask import jsonify, request, current_app
from app.models.stories import Story
from app.api import api
from app import db


@api.route('/stories/', methods=['GET'])
def get_stories():
    # Used for retrieving all stories
    current_app.logger.info('Retrieving all stories')
    current_app.logger.debug('This is a debug log')
    stories = Story.query.all()
    return jsonify({
        'stories': [story.to_half_json() for story in stories]
    })


@api.route('/stories/<int:id>', methods=['GET'])
def get_story(id):
    # Used for retrieving a story with a specific ID
    story = Story.query.get_or_404(id)
    current_app.logger.info('Retrieving story {}'.format(id))
    return jsonify(story.to_full_json())


@api.route('/stories/', methods=['POST'])
def new_story():
    # Used for creating a new story
    story = Story.from_json(request.json)
    current_app.logger.info('Creating new story')
    db.session.add(story)
    db.session.commit()
    return jsonify(story.to_full_json()), 201


@api.route('/stories/<int:id>', methods=['PUT'])
def edit_story(id):
    # Used for editing a story
    story = Story.query.get_or_404(id)
    story.title = request.json.get('title')
    story.topic = request.json.get('topic')
    story.text = request.json.get('text')
    story.author = request.json.get('author')

    current_app.logger.info('Editing story {}'.format(id))
    db.session.add(story)
    db.session.commit()
    return jsonify(story.to_full_json())
