"""This is where we create a function for initiating the application, which is
later on used at the very top level stories.py module to initiate the
application with a specific config file"""

# Flask Imports
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask import Flask

# Importing configs
from config import config_dict

# Setup

# We iniate the database and other packages that are going to play together
# with the app here

# For the database
db = SQLAlchemy()
# For database migrations
migrate = Migrate()
# For HTML bootstrapping
bootstrap = Bootstrap()


def create_app(config_key='local'):
    app = Flask(__name__)
    # Enabling config initiation
    app.config.from_object(config_dict[config_key])
    config_dict[config_key].init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    # Registering the main and the api blueprints here
    from app.main import main as main_blueprint
    from app.api import api as api_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    return app
