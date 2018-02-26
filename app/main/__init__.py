"""Initiates the main through Flask's blueprint"""

from flask import Blueprint

main = Blueprint('main', __name__)

# Similar to the API route import, in this case we need to import the views
# so it can be registered through the main blueprint.
from app.main import views
