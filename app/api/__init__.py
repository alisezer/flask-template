"""Initiates the API through Flask's blueprint"""

from flask import Blueprint
api = Blueprint('api', __name__)

# This import might seem unconventional, however is required to register your
# routes, which are created under the api folder. As you add more routes,
# you should import them here so the app can pick it up.

from app.api import stories
